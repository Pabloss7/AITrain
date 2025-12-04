import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
import xgboost as xgb


warnings.filterwarnings("ignore")

matches = pd.read_parquet("../data/matches_clean_dataset.parquet")

# We split the result of the game so we want to predict who will win
x, y = matches.drop(columns=["win"]), matches["win"]

#Split data into train and test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

dtrain_reg = xgb.DMatrix(x_train, y_train, enable_categorical=True)
dtest_reg = xgb.DMatrix(x_test, y_test, enable_categorical=True)



# Define hyperparameters
params = {"objective": "reg:squarederror", "tree_method": "gpu_hist"}

# Number of boosting rounds
n = 100
model = xgb.train(
   params=params,
   dtrain=dtrain_reg,
   num_boost_round=n,
)
print(matches.dtypes)