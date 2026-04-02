import os
from pymongo import MongoClient
import json
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging for database
logger = logging.getLogger("tripxplo-db")
logger.setLevel(logging.INFO)

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = "tripxplo_ai"

client = None
db = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        logger.info("Successfully connected to MongoDB.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB URI provided in .env: {e}")
        client = None

def get_hotels_data():
    """Returns hotels from Mongo if available, else JSON fallback."""
    if client is not None and db is not None:
        try:
            hotels = list(db.hotels.find({}, {"_id": 0}))
            if hotels:
                logger.debug(f"Retrieved {len(hotels)} hotels from MongoDB.")
                return hotels
        except Exception as e:
            logger.error(f"Error querying MongoDB: {e}")
            
    # Fallback to local JSON
    db_file = 'data/hotels.json'
    if os.path.exists(db_file):
        with open(db_file, 'r') as f:
            return json.load(f)
    return []

def save_hotels_data(hotels):
    """Saves to Mongo + JSON fallback."""
    os.makedirs('data', exist_ok=True)
    try:
        with open('data/hotels.json', 'w') as f:
            json.dump(hotels, f, indent=4)
        logger.info("Successfully mirrored database to data/hotels.json.")
    except Exception as e:
        logger.error(f"Failed to save JSON fallback: {e}")
        
    if client is not None and db is not None:
        try:
            # Clear and replace for simplicity in prototype
            db.hotels.delete_many({})
            db.hotels.insert_many(hotels)
            logger.info(f"Synchronized {len(hotels)} hotels into MongoDB collection.")
        except Exception as e:
            logger.error(f"Failed to synchronize data with MongoDB: {e}")
