import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_USER    = os.environ.get("MONGO_USER")
MONGO_PASS    = os.environ.get("MONGO_PASS")
METADATA_PATH = os.environ.get("METADATA_PATH")


# Connect to MongoDB
client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/')

#Access the database (create if it does not exist)
db = client['big_data_project']

#add collection to store image metadata
patients_collection = db['image_metadata']

#import dataset from csv file using pandas
meta = pd.read_csv(METADATA_PATH)
meta = meta[~meta.image.str.contains('downsampled')]

# Convert DataFrame to a list of dictionaries with column names as keys and value for each row as attribute
metadata = meta.to_dict(orient='records')

#insert multiple rows into MongoDB
patients_collection.insert_many(metadata)