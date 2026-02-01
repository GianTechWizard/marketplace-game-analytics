from pymongo import MongoClient
from datetime import datetime
from config.mongo_config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def daily_sales():
    pipeline = [
        {
            "$addFields": {
                "order_date_converted": {
                    "$toDate": "$order_date"
                }
            }
        },
        {
            "$lookup": {
                "from": "payments",
                "localField": "order_id",
                "foreignField": "order_id",
                "as": "payment"
            }
        },
        {"$unwind": "$payment"},
        {"$match": {"payment.payment_status": "SUCCESS"}},
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": {
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$order_date_converted"
                        }
                    }
                },
                "total_revenue": {
                    "$sum": {
                        "$multiply": ["$items.quantity", "$items.price"]
                    }
                },
                "total_orders": {"$addToSet": "$order_id"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": "$_id.date",
                "total_revenue": 1,
                "total_orders": {"$size": "$total_orders"},
                "generated_at": datetime.utcnow()
            }
        },
        {
            "$merge": {
                "into": "sales_daily_summary",
                "whenMatched": "replace",
                "whenNotMatched": "insert"
            }
        }
    ]

    db.orders_raw.aggregate(pipeline)
    print("✅ sales_daily_summary updated")

def run_all():
    daily_sales()
