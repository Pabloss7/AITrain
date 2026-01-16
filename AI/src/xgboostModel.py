import pandas as pd
import warnings
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.model_selection import GridSearchCV
import os
import joblib

warnings.filterwarnings("ignore")

matches = pd.read_parquet("./data/matches_clean_dataset.parquet")


# We split the result of the game so we want to predict who will win
x, y = matches.drop(columns=["win"]), matches["win"]

#Split data into train and test
x_train, x_test, y_train, y_test = train_test_split(
   x, y, test_size=0.2, random_state=42, stratify=y
   )
x_train.to_parquet("data/x_train.parquet", index=False)

xgb = XGBClassifier(
   objective="binary:logistic",
   tree_method="hist",
   device="cuda",
   eval_metric="auc",
   random_state=42
)

param_grid = {
   "max_depth": [3,5,7],
   "learning_rate": [0.01,0.05,0.1],
   "n_estimators": [300,600,1000],
   "subsample": [0.8,1.0],
   "colsample_bytree": [0.8,1.0]
}

grid = GridSearchCV(
   estimator=xgb,
   param_grid=param_grid,
   scoring="roc_auc",      # metric
   cv=5,                   # 5-fold cross-validation
   verbose=2,
   n_jobs=-1               #cores
)
grid.fit(x_train, y_train)

best_model = grid.best_estimator_


print("Best parameters found:")
print(grid.best_params_)

print(f"Best CV AUC: {grid.best_score_:.4f}")


os.makedirs("models",exist_ok=True)
joblib.dump(best_model, "models/xgboost_model_tuned.joblib")
best_model.get_booster().save_model("models/xgboost_model.json")

probs = best_model.predict_proba(x_test)[:,1]
preds = (probs >= 0.5).astype(int)

acc = accuracy_score(y_test, preds)
auc = roc_auc_score(y_test, probs)

print(f"Accuracy of the base model: {acc:.3f}")
print(f"AUC of the base model: {auc:.3f}")
print("\nClassification report:\n", classification_report(y_test, preds))
