import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

df = pd.read_parquet("../../data/matches_dataset.parquet")

# Erase matches shorter tahn 5 minutes
df = df[df.gameDuration > 300]

#We make sure there is no troll players
df = df[df.totalMinionsKilled > 10]
df = df[df.goldEarned > 2000]


# Add game duration in minutes
df["minutesDuration"] = df.gameDuration/60
df = df.drop(columns=["gameDuration"], errors="ignore")

# Add cs farmed per minute in game
df["CSMin"] = df.totalMinionsKilled/df.minutesDuration
df = df.drop(columns=["totalMinionsKilled"], errors="ignore")

# Add gold per minute
df["goldMin"] = df.goldEarned/df.minutesDuration
df = df.drop(columns=["goldEarned"], errors="ignore")

#Add damage per minute
df["dmgMin"] = df.totalDamageDealtToChampions/df.minutesDuration
df = df.drop(columns=["totalDamageDealtToChampions"], errors="ignore")

#Add vision score per minute
df["visionMin"] = df.visionScore/df.minutesDuration
df = df.drop(columns=["visionScore"], errors="ignore")
df = df.drop(columns=["wardsPlaced"], errors="ignore")
df = df.drop(columns=["wardsKilled"], errors="ignore")

#Delete the columns that are not useful but we thoought they were
#In case of championname and individual position we are droping the columns because they are
# breaking shap, so we will be handling in other way than expected
df = df.drop(columns=["firstBloodKill","championName","individualPosition"], errors="ignore")

#Convert booleans into number
df["win"] = df.win.astype(int)



# Now we apply normalization so the ML algorithm can learn better and faster
scaler = StandardScaler()
columns = ["goldMin", "dmgMin", "visionMin", "CSMin"]
df[columns] = scaler.fit_transform(df[columns])
joblib.dump(scaler, "../../data/standard_scaler.joblib")

print(df.dtypes)

df = df.reset_index(drop=True)
df.to_parquet("../../data/matches_clean_dataset.parquet", index=False)
