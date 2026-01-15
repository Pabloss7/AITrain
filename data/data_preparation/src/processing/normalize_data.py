import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
df = pd.read_parquet("../../data/matches_dataset_extended.parquet")

# ----------------------------
# BASIC CLEANING
# ----------------------------

# Remove very short games (< 5 min)
df = df[df.gameDuration > 300]

# Remove obvious trolls / corrupted data
df = df[df.totalMinionsKilled > 10]
df = df[df.goldEarned > 2000]

# ----------------------------
# CATEGORICAL ENCODING
# ----------------------------

# Drop champion name to avoid bias
df = df.drop(columns=["championName"], errors="ignore")

categorical_ohe = [
    "teamPosition",
    "individualPosition",
    "lane",
    "role",
]

df = pd.get_dummies(
    df,
    columns=[c for c in categorical_ohe if c in df.columns],
    drop_first=False
)

# ----------------------------
# TIME NORMALIZATION
# ----------------------------

# Game duration in minutes
df["minutesDuration"] = df.gameDuration / 60
df = df.drop(columns=["gameDuration"], errors="ignore")

# Per-minute metrics
df["dmgMin"] = df.totalDamageDealtToChampions / df.minutesDuration


# Drop raw absolute metrics
df = df.drop(
    columns=[
        "totalMinionsKilled",
        "goldEarned",
        "totalDamageDealtToChampions",
        "visionScore",
        "wardsPlaced",
        "wardsKilled",
    ],
    errors="ignore"
)

# ----------------------------
# BOOLEAN / BINARY FEATURES
# ----------------------------

bool_columns = df.select_dtypes(include="bool").columns
df[bool_columns] = df[bool_columns].astype(int)


# ----------------------------
# NUMERICAL SCALING
# ----------------------------

# Only scale continuous numerical features
scalable_features = [
  # Combat
    "kills","deaths","assists",
    "doubleKills","tripleKills","quadraKills","pentaKills",
    "largestKillingSpree","largestMultiKill",

    # Damage
    "physicalDamageDealtToChampions",
    "magicDamageDealtToChampions",
    "trueDamageDealtToChampions",
    "damageDealtToObjectives",
    "damageDealtToBuildings",
    "totalDamageTaken",
    "damageSelfMitigated",

    # Healing & CC
    "totalHeal","totalHealsOnTeammates",
    "totalTimeCCDealt","timeCCingOthers",

    # Economy & farm
    "goldSpent","goldPerMinute",
    "neutralMinionsKilled",
    "totalAllyJungleMinionsKilled",
    "totalEnemyJungleMinionsKilled",
    "csPerMinute",

    # Vision
    "visionScorePerMinute",

    # Objectives
    "turretKills","inhibitorKills",
    "dragonKills","baronKills",
    "objectivesStolen","objectivesStolenAssists",

    # Game length
    "minutesDuration","dmgMin"
]
#TODO: scale only the necessaty features
scaler = StandardScaler()
df[scalable_features] = scaler.fit_transform(df[scalable_features])

# Save scaler for inference
joblib.dump(scaler, "../../data/standard_scaler.joblib")

# ----------------------------
# FINAL DATASET
# ----------------------------
print(df.head(1))
print(df.dtypes)
df = df.reset_index(drop=True)
df.to_parquet("../../data/matches_clean_dataset.parquet", index=False)

print("Dataset ready ✅")
print(df.dtypes)
print(df.columns.tolist())