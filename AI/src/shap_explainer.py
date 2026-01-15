import pandas as pd
import shap 
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib
import traceback

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

        model_path = os.path.join(base_path(), "models", "xgboost_model_tuned.joblib")

        model = joblib.load(model_path)
        booster = model.get_booster()
        feature_columns = X.columns.tolist()

        explainer = shap.TreeExplainer(
            booster,
            data=background,
            feature_perturbation="interventional"
            )
        return explainer, feature_columns
    except Exception as e:
        traceback.print_exc()


def explain_match(single_match_features):
    explainer, feature_columns = load_explainer()
    X = single_match_features.to_numpy(dtype=np.float64)
   
    shap_values = explainer.shap_values(
        X,
        check_additivity=False
    )[0]
    print("Shap values obtained")
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