from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from shap_explainer import explain_match
from recommendations import generate_recommendation
from preprocessing import preprocess_player_match

app = FastAPI(
    title="Match AI recommendation system",
    version="1.0.0"
)


### REQUEST BODY
class MatchRequest(BaseModel):
    gameDuration: float
    championName: str
    individualPosition: str
    kills: int
    deaths: int
    assists: int
    minutesDuration: float
    CSMin: float
    goldMin: float
    dmgMin: float
    visionMin: float

### EDNPOINTS
@app.post("analyze-match")
def analyze_match(match: MatchRequest):
    df = pd.DataFrame([match.dict()])

    df_processed = preprocess_player_match(df, X.columns)

    top_features = explain_match(df_processed, explainer)

    recommendations = []
    for feature, value, shap_value in top_features:
        rec = generate_recommendation(feature, value, shap_value)
        if rec:
            recommendations.append({
                "feature": feature,
                "value": value,
                "shap_value": shap_value,
                "recommendation": rec
            })
        
    return {"recommendations": recommendations}
