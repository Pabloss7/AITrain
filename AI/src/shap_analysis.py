import pandas as pd
import shap 
import xgboost as xgb
import matplotlib.pyplot as plt

matches = pd.read_parquet("../data/matches_clean_dataset.parquet")

X = matches.drop(columns=["win"])

# Loads the model previously trained
model = xgb.Booster()
model.load_model("models/xgboost_model.json")

explainer = shap.TreeExplainer(
    model,
    feature_perturbation="tree_path_dependent"
    )
print(matches.dtypes)
shap_values = explainer.shap_values(X, check_additivity=False)

print(shap.summary_plot(shap_values, X))