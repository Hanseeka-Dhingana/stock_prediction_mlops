import os
import sys
import pandas as pd
import pickle
import pymongo
from dotenv import load_dotenv
from sklearn.metrics import mean_absolute_error


load_dotenv()

# --- MongoDB Configuration ---
# Replace with your actual connection string if using cloud (e.g., MongoDB Atlas)
MONGO_URI = os.getenv("MONGO_URL")

if not MONGO_URI:
    print("WARNING: MONGO_URL not found in .env file. Using localhost.")
    MONGO_URI = "mongodb://localhost:27017/"

DB_NAME = "stock_db"
COLLECTION_NAME = "features"

# Utility function to save objects (like the Scaler) using pickle
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise Exception(f"Error saving object: {e}")


# This function can be used to store the features in MongoDB after transformation.
def push_to_feature_store(df):
    try:
        print("Connecting to MongoDB Feature Store...")
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Reset index to ensure Date is saved as a column, not an index
        data_to_save = df.copy()
        if isinstance(data_to_save.index, pd.DatetimeIndex):
            data_to_save.reset_index(inplace=True)

        # Convert DataFrame to Dictionary records for MongoDB
        records = data_to_save.to_dict("records")

        # Overwrite existing data (Clear old history to avoid duplicates)
        collection.delete_many({})
        
        # Insert new features
        collection.insert_many(records)
        print(f"Successfully pushed {len(records)} feature rows to MongoDB!")

    except Exception as e:
        raise Exception(f"Error pushing to MongoDB: {e}")


# This function can be used in the Prediction Pipeline to pull the latest features for prediction
def pull_from_feature_store():
    try:
        print("Connecting to MongoDB Feature Store...")
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Fetch all data (exclude the internal '_id' field)
        cursor = collection.find({}, {'_id': 0})
        
        # Convert to DataFrame
        df = pd.DataFrame(list(cursor))
        
        if df.empty:
            raise Exception("Feature Store is empty! Run Data Transformation first.")

        print(f"Successfully pulled {len(df)} rows from MongoDB.")
        return df

    except Exception as e:
        raise Exception(f"Error pulling from MongoDB: {e}")