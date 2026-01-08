import pandas as pd
import matplotlib.pyplot as plt
import joblib
import mpl_toolkits.mplot3d
from sklearn.decomposition import PCA


df = pd.read_parquet("../data/matches_clean_dataset.parquet")
# TODO: fix standard scaler for all features(?)
features = [
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
    "csPerMinute","CSMin",

    # Vision
    "visionScorePerMinute",

    # Objectives
    "turretKills","inhibitorKills",
    "dragonKills","baronKills",
    "objectivesStolen","objectivesStolenAssists",

    # Early game
    "firstBloodKill","firstBloodAssist",
    "firstTowerKill","firstTowerAssist",

    # Roles / positions (one-hot)
    "teamPosition_BOTTOM","teamPosition_JUNGLE","teamPosition_MIDDLE",
    "teamPosition_TOP","teamPosition_UTILITY",

    "individualPosition_BOTTOM","individualPosition_JUNGLE",
    "individualPosition_MIDDLE","individualPosition_TOP",
    "individualPosition_UTILITY",

    "lane_BOTTOM","lane_JUNGLE","lane_MIDDLE","lane_TOP",

    "role_CARRY","role_SOLO","role_SUPPORT",

    # Game length
    "minutesDuration","dmgMin"
]

X = df[features]
y = df["win"]

# Escalado
scaler = joblib.load("../models/standard_scaler_all_features.joblib")
X_scaled = scaler.transform(X)

# PCA en 2D
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)

# Plot 2D
plt.figure(figsize=(8,6))
scatter = plt.scatter(
    X_reduced[:,0],
    X_reduced[:,1],
    c=y,
    s=15,
    alpha=0.6
)

plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
plt.title("PCA 2D – Player Performance Projection")

legend = plt.legend(
    scatter.legend_elements()[0],
    ["Loss","Win"],
    title="Match outcome"
)
plt.gca().add_artist(legend)

plt.tight_layout()
plt.savefig("../figures/pca_2d_all_features.png", dpi=300)
plt.close()

# Varianza
print("Explained variance:", pca.explained_variance_ratio_)

# Loadings
loadings = pd.DataFrame(
    pca.components_,
    columns=features,
    index=["PC1","PC2"]
)

print(loadings.T.sort_values("PC1", ascending=False).head(10))
