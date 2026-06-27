import pandas as pd
import shap 
import matplotlib.pyplot as plt
import numpy as np
import os
import traceback
from xgboost import Booster
from src.models.role_feature_map import ROLE_FEATURE_MAP

explainer = None
feature_columns = None

def base_path():
    return os.path.dirname(__file__)

def load_matrix():
    path = os.path.join(base_path(), "data", "x_train.parquet")
    return pd.read_parquet(path)

def load_explainer():
    try:
        global explainer, feature_columns

        if explainer is not None:
            return explainer, feature_columns
        
        X = load_matrix()

        background = shap.sample(X, 100).to_numpy(dtype=np.float64)

        model_path = os.path.join(base_path(), "models", "xgboost_model.json")

        booster = Booster()
        booster.load_model(model_path)
        feature_columns = X.columns.tolist()

        explainer = shap.TreeExplainer(
            booster,
            data=background,
            feature_perturbation="interventional"
            )
        return explainer, feature_columns
    except Exception as e:
        traceback.print_exc()
        raise e

def explain_match(single_match_features, role, max_features=3, epsilon=0.01):
    explainer, feature_columns = load_explainer()
    
   
    single_match_features = single_match_features.reindex(
        columns=feature_columns,
        fill_value=0
    )
    assert single_match_features.shape[1] == len(feature_columns)
    X = single_match_features.to_numpy(dtype=np.float64)
    

    shap_values = explainer.shap_values(
        X,
        check_additivity=False
    )[0]

    # DEBUG: Print all SHAP values for role-relevant features
    role_features = ROLE_FEATURE_MAP.get(role, {})
    print(f"\n=== DEBUG SHAP for role={role} ===")
    print(f"Top 10 features by |SHAP| (any role):")
    debug_sorted = np.argsort(np.abs(shap_values))[::-1]
    for rank, idx in enumerate(debug_sorted[:10]):
        feat = feature_columns[idx]
        sv = shap_values[idx]
        in_role = "(MAPPED)" if feat in role_features else ""
        print(f"  #{rank+1}: {feat} = {sv:.4f} {in_role}")
    
    print(f"\nRole-mapped features for {role}:")
    for feat, aspect in role_features.items():
        if feat in feature_columns:
            feat_idx = feature_columns.index(feat)
            sv = shap_values[feat_idx]
            val = single_match_features.iloc[0, feat_idx]
            print(f"  {feat} -> {aspect}: SHAP={sv:.4f}, value={val:.4f}")
        else:
            print(f"  {feat} -> {aspect}: NOT IN MODEL COLUMNS")
    print("=== END DEBUG ===\n")

    selected = []
    used_aspects = set()

    sorted_idx = np.argsort(np.abs(shap_values))[::-1]

    for i in sorted_idx:
        
        shap_val = shap_values[i]
        feature = feature_columns[i]
        #solo impacto negativo
        if shap_val >= 0:
            continue

        # umbral mínimo
        if abs(shap_val) < epsilon:
            continue

        # feature relevante para el rol
        if feature not in ROLE_FEATURE_MAP.get(role, {}):
            continue

        aspect = ROLE_FEATURE_MAP[role][feature]

        #evitar redundancia
        if aspect in used_aspects:
            continue

        selected.append(
            (
                feature,
                single_match_features.iloc[0, i],
                shap_val,
                aspect
            )
        )
        used_aspects.add(aspect)
        
        if len(selected) == max_features:
            break
    print(selected)
    return selected
