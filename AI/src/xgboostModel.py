import pandas as pd
import warnings
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.preprocessing import StandardScaler
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


model = XGBClassifier(
   objective="binary:logistic",
   tree_method="hist",
   eval_metric="auc",
   n_estimators=2000,
   early_stopping_rounds=100
)

model.fit(
   x_train,
   y_train,
   eval_set=[(x_test, y_test)],
   verbose=100
)
os.makedirs("models",exist_ok=True)
model.save_model("models/xgboost_model.bin")


probs = model.predict_proba(x_test)[:,1]
preds = (probs >= 0.5).astype(int)

acc = accuracy_score(y_test, preds)
auc = roc_auc_score(y_test, probs)
print(f"Accuracy of the base model: {acc:.3f}")
print(f"AUC of the base model: {auc:.3f}")
print("\nClassification report:\n", classification_report(y_test, preds))


#rmse = mean_squared_error(y_test, preds, squared=False)
#print(f"RMSE of the base model: {rmse:.3f}")
#results = xgb.cv(
#   params,dtrain_reg,
#   num_boost_round=n,
#   nfold=5,
#   early_stopping_rounds=20
#)
#print(results.head())
#best_rmse = results['test-rmse-mean'].min()
#print(f"Best RMSE: {best_rmse:.3f}")
