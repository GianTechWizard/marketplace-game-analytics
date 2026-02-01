import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

NUM_USERS = 20
NUM_GAMES = 10
NUM_ORDERS = 50

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 1, 10)

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

# ---------- USERS ----------
users = []
for i in range(1, NUM_USERS + 1):
    users.append({
        "user_id": f"U{i:03}",
        "username": fake.user_name(),
        "email": fake.email(),
        "country": random.choice(["Indonesia", "Singapore", "Malaysia"]),
        "created_at": fake.date_time_this_year().isoformat(),
        "is_active": True
    })

# ---------- GAMES ----------
genres = ["RPG", "Action", "Adventure", "Simulation"]
games = []
for i in range(1, NUM_GAMES + 1):
    games.append({
        "game_id": f"G{i:03}",
        "title": fake.catch_phrase(),
        "genre": random.choice(genres),
        "developer": fake.company(),
        "price": random.randint(50000, 300000),
        "release_date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
        "is_active": True
    })

# ---------- ORDERS & PAYMENTS ----------
orders = []
payments = []

for i in range(1, NUM_ORDERS + 1):
    order_date = random_date(START_DATE, END_DATE)
    user = random.choice(users)
    game = random.choice(games)
    qty = random.randint(1, 2)

    order_id = f"O{i:04}"

    orders.append({
        "order_id": order_id,
        "user_id": user["user_id"],
        "order_date": order_date.isoformat(),
        "items": [
            {
                "game_id": game["game_id"],
                "quantity": qty,
                "price": game["price"]
            }
        ],
        "order_status": "COMPLETED",
        "created_at": order_date.isoformat()
    })

    status = random.choices(["SUCCESS", "FAILED"], weights=[0.8, 0.2])[0]

    payments.append({
        "payment_id": f"P{i:04}",
        "order_id": order_id,
        "payment_method": random.choice(["E-Wallet", "Credit Card"]),
        "payment_status": status,
        "paid_amount": game["price"] * qty if status == "SUCCESS" else 0,
        "paid_at": order_date.isoformat()
    })

# ---------- SAVE ----------
def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

save("data/raw/users.json", users)
save("data/raw/games.json", games)
save("data/raw/orders.json", orders)
save("data/raw/payments.json", payments)
print("Dummy data berhasil dibuat")
