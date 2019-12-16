import pymongo
import pandas as pds

client = pymongo.MongoClient()

def upsert_nba(df):
    db = client.get_database("nba")
    collection = db.get_collection("energy")
    for record in df.to_dict('records'):
        collection.replace_one(
            filter={'Player': record['Player']},
            replacement=record,
            upsert = True)

def fetch_all_nba():
    db = client.get_database("nba")
    collection = db.get_collection("energy")
    return list(collection.find())

if __name__ == "__main__":
    print(fetch_all_nba())
