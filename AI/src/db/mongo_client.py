from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def insert_mongo_response(jobId, response):
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_RECOMS_COLLECTION")

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    collection.insert_one({
        "jobId": jobId,
        "status": "completed",
        "recommendations": response
    })

def get_mongo_recommendation(jobId):
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_RECOMS_COLLECTION")

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    return collection.find_one({"jobId": jobId})
