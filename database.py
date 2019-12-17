import pymongo
import pandas as pds
import time

client = pymongo.MongoClient()

def upsert_nba(data):
    db = client.get_database("nba")
    collection = db.get_collection("nba")
    for record in data:
        collection.replace_one(
            filter={'Player': record['Player']},
            replacement=record,
            upsert = True)

def fetch_all_nba():
    db = client.get_database("nba")
    collection = db.get_collection("nba")
    return list(collection.find())

def to_df():
    """Converts list of dict to DataFrame"""
    data = fetch_all_nba()
    if len(data) == 0:
        time.sleep(5) # wait for 5 seconds for database completion
        return to_df()
    df = pds.DataFrame.from_records(data)
    df.drop("_id", axis=1, inplace=True)
    return df

if __name__ == "__main__":
    print(to_df())
