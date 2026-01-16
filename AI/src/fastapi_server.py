import httpx
import traceback
import pandas as pd
import numpy as np
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from dotenv import load_dotenv

from src.shap_explainer import explain_match
from src.recommendations import generate_recommendation
from src.preprocessing import preprocess_player_match
from src.models.requestModels import MatchProcessRequest
from src.processing.extract_metrics import extract_metrics, extract_metrics_player
from src.processing.clean_data import clean_dataset
from src.processing.normalize_data import normalize_data
from src.db.mongo_client import insert_mongo_response, get_mongo_recommendation
from src.utils.data_conversor import to_python_type

app = FastAPI(
    title="Match AI recommendation system",
    version="1.0.0"
)

load_dotenv()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    print("VALIDATION ERROR DETECTED")
    print(exc.errors())
    print("BODY:")
    print(body.decode()) 
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": body.decode()
        }
    )

async def notify_core(job_id: str):
    core_url = os.getenv("CORE_URL")
    url= f"{core_url}/{job_id}/completed"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(url)
            response.raise_for_status()
            print("Core communication:", response.status_code)
        except httpx.HTTPError as e:
            print("Error with Core microservice:", e)

### EDNPOINTS
@app.post("/analyze-match", status_code=201)
async def analyze_match(match: MatchProcessRequest):
    try:
        metrics = extract_metrics_player(match.info,match.metadata, match.puuid)

        df = clean_dataset(metrics)
        df = normalize_data(df)
        
        columns = os.getenv("COLUMNS").split(",")
        df_processed = preprocess_player_match(df, columns)
        
        print("Data processed")
        #df_processed = df_processed.astype(np.float64)
        top_features = explain_match(df_processed)
        print("Explainer processed")
        
        recommendations = []
        for feature, value, shap_value in top_features:
            rec = generate_recommendation(feature, value, shap_value)
            if rec:
                recommendations.append({
                    "feature": feature,
                    "value": to_python_type(value),
                    "shap_value": to_python_type(shap_value),
                    "recommendation": rec
                })
        # NOTE: It's important to save in db before notifying core, so we avoid race conditions
        # Persist first → avoid race condition
        insert_mongo_response(match.jobId, recommendations)
        await notify_core(match.jobId)
        return {"message": "Match processed"}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"message": "Error processing match", "error": str(e)}
        )    


@app.get("/recommendations/{job_id}")
async def get_recommendations(job_id: str, request: Request):
    recomms = get_mongo_recommendation(job_id)
    if recomms is None:
        return {"error": "Job not found"}, 404
    return recomms


@app.post("/analyze-match-debug")
async def debug_endpoint(request: Request):
    body = await request.json()
    print("received:")
    print(body)
    return {"ok": True}
