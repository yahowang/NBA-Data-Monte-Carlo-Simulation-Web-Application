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

def to_df():
    """Converts list of dict to DataFrame"""
    data = fetch_all_nba()
    if len(data) == 0:
        return None
    df  = pds.DataFrame.from_records(data)
    df.drop("_id", axis=1, inplace=True)
    return df

if __name__ == "__main__":
    print(to_df())
