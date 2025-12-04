import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split


warnings.filterwarnings("ignore")

matches = pd.read_parquet("../data/matches_clean_dataset.parquet")

x, y = matches.drop(columns=["win"]), matches["win"]


print(matches.describe(exclude=np.number))