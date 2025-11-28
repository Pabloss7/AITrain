from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_mongo_collection():
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB")
        collection_name = os.getenv("MONGO_COLLECTION")
        
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        return collection