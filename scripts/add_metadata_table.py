import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
METADATA_PATH = os.environ.get("METADATA_PATH")


# Connect to MongoDB
client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/')

#create database
db = client['big_data_project']

#add collection to store image metadata
patients_collection = db['image_metadata']

#import dataset from csv file using pandas
patients_df = pd.read_csv(METADATA_PATH)

# Convert DataFrame to a list of dictionaries
patients_data = patients_df.to_dict(orient='records')

#insert multiple rows into MongoDB
patients_collection.insert_many(patients_data)