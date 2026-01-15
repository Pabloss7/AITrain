import joblib

path = "models/standard_scaler.joblib"
scaler = joblib.load(path)

# Columnas que el scaler vio en entrenamiento
print("Número de columnas esperadas:", len(scaler.feature_names_in_))
print("Primeras 10 columnas esperadas:", scaler.feature_names_in_)
