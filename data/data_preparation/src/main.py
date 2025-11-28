from db.mongo_client import get_mongo_collection
from processing.clean_data import clean_dataset
from processing.extract_metrics import extract_metrics

def main():
    collection = get_mongo_collection()
    
    cursor = collection.find({}, batch_size=500)
    rows = []
    
    for match in cursor:
        metrics = extract_metrics(match)
        rows.append(metrics)
        
        
    df = clean_dataset(rows)
    
    df.to_parquet("data/matches.")    
    