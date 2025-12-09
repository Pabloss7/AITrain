import pandas as pd
import shap 
import xgboost as xgb
import matplotlib.pyplot as plt
import numpy as np

matches = pd.read_parquet("../data/matches_clean_dataset.parquet")
categorical_columns = ["championName", "individualPosition"]

matches_encoded = pd.get_dummies(matches, columns=categorical_columns)

X = matches_encoded.drop(columns=["win"])

background = shap.sample(X, 100)

model = xgb.Booster()
model.load_model("../models/xgboost_model.json")

explainer = shap.TreeExplainer(
    model,
    data=background,
    feature_perturbation="interventional"
    )

def explain_match(single_match_features):
    shap_values = explainer.shap_values(single_match_features)
    
    sorted_idx = np.argsort(np.abs(shap_values))[::-1][:5]

    top_features = [
    (X.columns[i], single_match_features[i], shap_values[i])
    for i in sorted_idx
    ]
    
    return top_features