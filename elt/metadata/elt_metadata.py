from pymongo import MongoClient
from datetime import datetime
from config.mongo_config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def update_metadata():
    db.elt_metadata.update_one(
        {"pipeline": "marketplace_game_elt"},
        {"$set": {"last_run": datetime.utcnow()}},
        upsert=True
    )
