import os
from pymongo import MongoClient
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = "tripxplo_ai"

client = None
db = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB Exception: {e}")
        client = None

def get_hotels_data():
    """Returns hotels from Mongo if available, else JSON fallback."""
    if client is not None and db is not None:
        try:
            hotels = list(db.hotels.find({}, {"_id": 0}))
            if hotels:
                return hotels
        except Exception as e:
            print(f"Failed to query Mongo: {e}")
            
    # Fallback to local JSON
    db_file = 'data/hotels.json'
    if os.path.exists(db_file):
        with open(db_file, 'r') as f:
            return json.load(f)
    return []

def save_hotels_data(hotels):
    """Saves to Mongo + JSON fallback."""
    os.makedirs('data', exist_ok=True)
    with open('data/hotels.json', 'w') as f:
        json.dump(hotels, f, indent=4)
        
    if client is not None and db is not None:
        try:
            # Clear and replace for simplicity in prototype
            db.hotels.delete_many({})
            db.hotels.insert_many(hotels)
            print("Saved mock data to MongoDB.")
        except Exception as e:
            print(f"Failed to insert to Mongo: {e}")
