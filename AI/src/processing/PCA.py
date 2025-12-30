import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


df = pd.read_parquet("../data/matches_clean_dataset.parquet")

features = [
    "goldPerMinute",
    "dmgMin",
    "visionScorePerMinute",
    "csPerMinute",
]

X = df[features]

scaler = joblib.load("../models/standard_scaler.joblib")
X_scaled = scaler.transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)


plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], alpha=0.7)

plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
plt.title("PCA, 2 components projection")

plt.tight_layout()
plt.savefig("../figures/pca_projection.png", dpi=300)
plt.close()

loadings = pd.DataFrame(
    pca.components_,
    columns=features,
    index=["PC1","PC2"]
)

print(loadings)