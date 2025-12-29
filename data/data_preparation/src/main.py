from .db.mongo_client import get_mongo_collection
from .processing.clean_data import clean_dataset
from .processing.extract_metrics import extract_metrics

def main():
    collection = get_mongo_collection()
    
    cursor = collection.find({}, batch_size=500)
    rows = []
    
    for match_doc in collection.find():
        participants = match_doc["json"]["info"]["participants"]

        if not participants or len(participants) < 10:
            print("Skipping match due to invalid data, match id: ", match_doc["_id"])
            collection.find_one_and_delete(match_doc)
            
    for match in cursor:
        metrics = extract_metrics(match)
        rows.extend(metrics)
        
        
    df = clean_dataset(rows)
    print(df.head(1))
    print(df.dtypes)
    df.to_parquet("data/matches_dataset_extended.parquet", index=False)


if __name__ == "__main__":
    main()
