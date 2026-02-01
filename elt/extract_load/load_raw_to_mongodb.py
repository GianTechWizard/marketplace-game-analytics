import json
from pymongo import MongoClient
from config.mongo_config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def load_json(path, collection_name, key):
    with open(path) as f:
        data = json.load(f)

    col = db[collection_name]
    for doc in data:
        col.update_one(
            {key: doc[key]},
            {"$set": doc},
            upsert=True
        )

    print(f"✅ {collection_name} loaded")

def load_all_raw():
    load_json("data/raw/users.json", "users", "user_id")
    load_json("data/raw/games.json", "games", "game_id")
    load_json("data/raw/orders.json", "orders_raw", "order_id")
    load_json("data/raw/payments.json", "payments", "payment_id")
