import json
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from dotenv import load_dotenv
import os
from src.shap_explainer import explain_match
from src.recommendations import generate_recommendation
from src.preprocessing import preprocess_player_match
from src.models.requestModels import MatchProcessRequest
from src.processing.extract_metrics import extract_metrics, extract_metrics_player
from src.processing.clean_data import clean_dataset
from src.processing.normalize_data import normalize_data
from src.db.mongo_client import insert_mongo_response
import httpx

app = FastAPI(
    title="Match AI recommendation system",
    version="1.0.0"
)

load_dotenv()

async def notify_core(job_id: str,core_url: str):
    payload = {"jobId": job_id, "status": "COMPLETED"}

    async with httpx.AsyncClient() as client:
        try:
            response: await client.post(core_url, json=payload)
            response.raise_for_status()
            print("Core communication:", response.status_code)
        except httpx.HTTPError as e:
            print("Error with Core microservice:", e)

### EDNPOINTS
@app.post("/analyze-match")
def analyze_match(match: MatchProcessRequest):
    try:
        metrics = extract_metrics_player(match.info,match.metadata, match.puuid)

        df = clean_dataset(metrics)
        df = normalize_data(df)
        categorical_columns = os.getenv("CATEGORICAL_COLUMNS").split(",")
        columns = os.getenv("COLUMNS").split(",")
        df_processed = preprocess_player_match(df, categorical_columns, columns)

        top_features = explain_match(df_processed)
        
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
        insert_mongo_response(match.jobId, recommendations)
        notify_core(match.jobId,"LA_URL_DEL_CORE")
        return {"message": "Match processed"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Error processing match", "error": str(e)}
        )    
