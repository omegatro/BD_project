import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
LABEL_PATH = os.environ.get("LABEL_PATH")


# Connect to MongoDB
client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/')

#create database
db = client['big_data_project']

#add collection to store image metadata
patients_collection = db['labels']

#import dataset from csv file using pandas
labels = pd.read_csv(LABEL_PATH)
labels = labels[~labels.image.str.contains('downsampled')]

# Convert DataFrame to a list of dictionaries with column names as keys and value for each row as attribute
patients_data = labels.to_dict(orient='records')

#insert multiple rows into MongoDB
patients_collection.insert_many(patients_data)