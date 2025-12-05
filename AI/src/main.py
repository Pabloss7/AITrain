import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OrdinalEncoder


warnings.filterwarnings("ignore")

matches = pd.read_parquet("../data/matches_clean_dataset.parquet")

# We split the result of the game so we want to predict who will win
x, y = matches.drop(columns=["win"]), matches["win"]
y_encoded =  OrdinalEncoder().fit_transform(y)
#Split data into train and test
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, random_state=1,stratify=y_encoded)


dtrain_reg = xgb.DMatrix(x_train, y_train, enable_categorical=True)
dtest_reg = xgb.DMatrix(x_test, y_test, enable_categorical=True)



# Define hyperparameters
params = {"objective": "reg:squarederror", "tree_method": "gpu_hist"}
# Number of boosting rounds
n = 1000

evaluations = [(dtrain_reg, "train"), (dtest_reg, "validation")]

model = xgb.train(
   params=params,
   dtrain=dtrain_reg,
   num_boost_round=n,
   evals=evaluations,
   verbose_eval=50,
   early_stopping_rounds=50
)

preds = model.predict(dtest_reg)

rmse = mean_squared_error(y_test, preds, squared=False)
print(f"RMSE of the base model: {rmse:.3f}")
results = xgb.cv(
   params,dtrain_reg,
   num_boost_round=n,
   nfold=5,
   early_stopping_rounds=20
)
print(results.head())
best_rmse = results['test-rmse-mean'].min()
print(f"Best RMSE: {best_rmse:.3f}")
