import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

df = pd.read_parquet("../data/matches_clean_dataset.parquet")

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
    "csPerMinute",

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

# ---------------- PCA ----------------
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# --------- Reconstrucción del rol ----------
role_map = {
    "teamPosition_TOP": "TOP",
    "teamPosition_JUNGLE": "JUNGLE",
    "teamPosition_MIDDLE": "MID",
    "teamPosition_BOTTOM": "BOT",
    "teamPosition_UTILITY": "SUPPORT"
}

df["role"] = (
    df[list(role_map.keys())]
    .idxmax(axis=1)
    .map(role_map)
)

# ---------------- Plot ----------------
plt.figure(figsize=(9, 7))

for role in df["role"].unique():
    mask = df["role"] == role
    plt.scatter(
        X_reduced[mask, 0],
        X_reduced[mask, 1],
        s=15,
        alpha=0.6,
        label=role
    )
# ---------------- Añadir Loadings (Biplot) ----------------
# ---------------- Loadings ----------------
loadings = pd.DataFrame(
    pca.components_,
    columns=features,
    index=["PC1","PC2"]
)
# Factor de escala para que las flechas se vean bien sobre los puntos
scale_factor = 30  

# Seleccionamos las variables con más impacto (puedes ajustar el top_n)
top_n = 8 
# Calculamos la magnitud del vector (distancia al origen) para cada variable
magnitudes = np.sqrt(loadings.loc["PC1"]**2 + loadings.loc["PC2"]**2)
important_features = magnitudes.sort_values(ascending=False).head(top_n).index

for feature in important_features:
    x_val = loadings.loc["PC1", feature] * scale_factor
    y_val = loadings.loc["PC2", feature] * scale_factor
    
    # Dibujar la flecha
    plt.arrow(0, 0, x_val, y_val, color='black', alpha=0.8, 
              width=0.05, head_width=0.3, zorder=10)
    
    # Añadir el texto con un pequeño offset
    plt.text(x_val * 1.15, y_val * 1.15, feature, color='black', 
             fontsize=10, fontweight='bold', ha='center', va='center',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'), zorder=11)

plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
plt.title("PCA 2D – Separación de jugadores por rol")

plt.legend(title="Rol")
plt.grid(alpha=0.2)

plt.tight_layout()
plt.savefig("../figures/pca_2d_all_features_by_rol_biplot.png", dpi=300)
plt.close()

# ---------------- Varianza ----------------
print("Explained variance:", pca.explained_variance_ratio_)



print(loadings.T.sort_values("PC1", ascending=False))
