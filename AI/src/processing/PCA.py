import pandas as pd
import matplotlib.pyplot as plt
import joblib
import mpl_toolkits.mplot3d
from sklearn.decomposition import PCA


df = pd.read_parquet("../data/matches_clean_dataset.parquet")

features = [
    "goldPerMinute",
    "dmgMin",
    "visionScorePerMinute",
    "csPerMinute"
]

X = df[features]
y = df["win"] #TARGET

scaler = joblib.load("../models/standard_scaler.joblib")
X_scaled = scaler.transform(X)


pca = PCA(n_components=3)
X_reduced = pca.fit_transform(X_scaled)

fig = plt.figure(1, figsize=(8,6))
ax = fig.add_subplot(111, projection="3d", elev=30, azim=45)

scatter = ax.scatter(
    X_reduced[:,0],
    X_reduced[:,1],
    X_reduced[:,2],
    c=y,
    s=40,
)

ax.set(
    title="First three principal components",
    xlabel=f"1st Component-{pca.explained_variance_ratio_[0]*100:.2f}%",
    ylabel=f"2nd Component-{pca.explained_variance_ratio_[1]*100:.2f}%",
    zlabel=f"3rd Component-{pca.explained_variance_ratio_[2]*100:.2f}%",
)

ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])

legend = ax.legend(
    scatter.legend_elements()[0],
    ["Loss","Win"],
    loc="upper right",
    title="Match outcome",
)
ax.add_artist(legend)

plt.tight_layout()
plt.savefig("../figures/pca_projection.png", dpi=300)
plt.close()

print("variance:\n",pca.explained_variance_ratio_)
loadings = pd.DataFrame(
    pca.components_,
    columns=features,
    index=[f"PC{i+1}" for i in range(pca.n_components_)]
)
print("loadings:\n", loadings)
