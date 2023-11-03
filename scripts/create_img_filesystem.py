import os
from pymongo import MongoClient
from concurrent.futures import ProcessPoolExecutor
from dotenv import load_dotenv
load_dotenv()
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
IMG_PATH = os.environ.get("IMG_PATH")
from gridfs import GridFS

# Connect to MongoDB
client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/')

db = client['big_data_project']
fs = GridFS(db, collection='images')


#define function to insert single image into mongodb
def process_image(filename):
    if filename.endswith('.jpg'):
        with open(os.path.join(IMG_PATH, filename), 'rb') as image_file:
            image_id = fs.put(image_file, filename=filename)

        # Update the existing metadata collection with the GridFS file ID
        db['image_metadata'].update_one(
            {'image': filename.replace('.jpg','')},  # Assuming filename without .jpg
            {'$set': {'gridfs_id': image_id}},
            upsert=True
        )

if __name__ == "__main__":
    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(process_image, filename) for filename in os.listdir(IMG_PATH)]
