import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_parquet("data/matches_dataset.parquet")

# Erase matches shorter tahn 5 minutes
df = df[df.gameDuration > 300]

#We make sure there is no troll players
df = df[df.totalMinionsKilled < 10]
df = df[df.goldEarned < 2000]

# Add KDA variable combining kills deaths and assists
df["KDA"] = (df.kills + df.assists)/df.deaths.replace(0,1)

# Add game duration in minutes
df["minutesDuration"] = df.gameDuration/60

# Add cs farmed per minute in game
df["CSMin"] = df.totalMinionsKilled/df.minutesDuration

# Add gold per minute
df["goldMin"] = df.goldEarned/df.minutesDuration

#Add damage per minute
df["dmgMin"] = df.totalDamageDealtToChampions/df.minutesDuration

#Add vision score per minute
df["visionMin"] = df.visionScore/df.minutesDuration
#Convert booleans into number
df["win"] = df.win.astype(int)
df["firstBloodKill"] = df.firstBloodKill.astype(int) 

#Ensure we have roles inside params
df = df[df.individualPosition.isin(["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"])]


# Now we apply normalization so the ML algorithm can learn better and faster
scaler = StandardScaler()
columns = ["KDA", "goldMin", "dmgMin", "visionMin", "CSMin"]
df[columns] = scaler.fit_transform(df[columns])



print(df)