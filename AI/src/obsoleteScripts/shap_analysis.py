import pandas as pd
import shap 
import xgboost as xgb
import matplotlib.pyplot as plt
import numpy as np

def generate_recommendation(feature, value, shap_val):
    if feature == "deaths":
        if shap_val < 0:
            return "Has muerto demasiado. Intenta jugar más seguro para mejorar tu impacto."
    
    if feature == "kills":
        if shap_val < 0:
            return "Has conseguido pocas kills. Busca mejores oportunidades de tradeo y presión."
        else:
            return "Buen número de kills. Tu agresividad ha sido beneficiosa."

    if feature == "assists":
        if shap_val < 0:
            return "Participa más en las peleas para aumentar tu número de asistencias."
        else:
            return "Gran participación en peleas. Sigue así."

    if feature == "goldMin":
        if shap_val < 0:
            return "Tu oro por minuto es bajo. Intenta mejorar tu farmeo o eficiencia en mapa."
        else:
            return "Excelente oro por minuto. Está siendo clave en tus victorias."

    if feature == "visionMin":
        if shap_val < 0:
            return "Tu score de visión es bajo. Mejora tu control de wards."
        else:
            return "Buen control de visión. Sigue manteniendo la presión."

    return None


matches = pd.read_parquet("../data/matches_clean_dataset.parquet")

categorical_columns = ["championName", "individualPosition"]
matches_encoded = pd.get_dummies(matches, columns=categorical_columns)

X, Y = matches_encoded.drop(columns=["win"]), matches_encoded["win"]

background = shap.sample(X, 100)

# Loads the model previously trained
model = xgb.Booster()
model.load_model("models/xgboost_model.json")

explainer = shap.TreeExplainer(
    model,
    data=background,
    feature_perturbation="interventional"
    )

#shap_values = explainer.shap_values(X)
#~Test individual recomendation
idx = 250
player_features = X.iloc[idx]
player_shap_values = explainer.shap_values(player_features)

sorted_idx = np.argsort(np.abs(player_shap_values))[::-1]

top_features = [
 (X.columns[i],player_features[i], player_shap_values[i])   
 for i in sorted_idx[:5]	
]

print(top_features)

recommendations = []
for feature, value, shap_val in top_features:
    rec = generate_recommendation(feature, value, shap_val)
    if rec:
        recommendations.append(rec)

for rec in recommendations:
    print(rec)



