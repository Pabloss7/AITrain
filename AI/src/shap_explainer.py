import pandas as pd
import shap 
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import numpy as np
import os

explainer = None
feature_columns = None

def base_path():
    return os.path.dirname(__file__)

def load_matches():
    path = os.path.join(base_path(), "data", "matches_clean_dataset.parquet")
    return pd.read_parquet(path)

def load_explainer():
    global explainer, feature_columns

    if explainer is not None:
        return explainer, feature_columns
    
    matches = load_matches()
    categorical_columns = ["championName", "individualPosition"]

    matches_encoded = pd.get_dummies(matches, columns=categorical_columns)

    X = matches_encoded.drop(columns=["win"])

    background = shap.sample(X, 100)

    model_path = os.path.join(base_path(), "models", "xgboost_model.json")

    model = xgb.Booster()
    model.load_model(model_path)

    feature_columns = X.columns.tolist()

    explainer = shap.TreeExplainer(
        model,
        data=background,
        feature_perturbation="interventional"
        )
    return explainer, feature_columns

#TODO: ARREGLAR EL PROBLEMA DE LAS COLUMNAS DE SHAP
def explain_match(single_match_features):
    explainer, feature_columns = load_explainer()

    shap_values = explainer.shap_values(single_match_features)[0]
    
    sorted_idx = np.argsort(np.abs(shap_values))[::-1][:5]

    top_features = [
        (
            feature_columns[i],
            single_match_features.iloc[0, i],
            shap_values[i]
        )
        for i in sorted_idx
    ]
    
    return top_features