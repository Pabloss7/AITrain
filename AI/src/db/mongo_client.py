from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def insert_mongo_response(jobId, response, aspect, role):
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_RECOMS_COLLECTION")

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    # Defensive handling of non-serializable response types
    clean_response = response
    
    # If it's a dict, try to extract the inner response string
    if isinstance(response, dict):
        clean_response = response.get("response", str(response))
    # If it's dict_values (common if someone does dict.values()), extract the first element
    elif hasattr(response, '__iter__') and not isinstance(response, (str, list, tuple)):
        try:
            val_list = list(response)
            clean_response = val_list[0] if val_list else ""
        except:
            clean_response = str(response)

    collection.insert_one({
        "jobId": jobId,
        "status": "completed",
        "response": clean_response,
        "aspect": aspect,
        "role": role
    })

def get_mongo_recommendation(jobId):
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_RECOMS_COLLECTION")

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    document = collection.find_one({"jobId": jobId})
    
    if document:
        document.pop("_id", None)
    return document
