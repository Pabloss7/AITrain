import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import joblib

def base_path():
    return os.path.dirname(os.path.dirname((__file__)))

def normalize_data(df):
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
    print("El df:", df.columns)

    # Now we apply normalization so the ML algorithm can learn better and faster
    path = os.path.join(base_path(),"models", "standard_scaler.joblib")
    scaler = joblib.load(path)

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
    df
    for col in scalable_features:
        if col not in df.columns:
            df[col] = 0

    df[scalable_features] = scaler.transform(df[scalable_features])

    # ----------------------------
    # FINAL DATASET
    # ----------------------------
    df = df.reset_index(drop=True)

    return df