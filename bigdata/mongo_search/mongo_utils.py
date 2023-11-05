#based on https://www.mongodb.com/compatibility/mongodb-and-django
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")


def get_mongo_db_handle():
    client = MongoClient(host=MONGO_HOST,
                        port=int(MONGO_PORT),
                        username=MONGO_USER,
                        password=MONGO_PASS
                        )
    return  client[MONGO_DB_NAME]


def get_metadata(age_range=None, sex=None, anatomical_sites=None, diagnosis_codes=None):
    db = get_mongo_db_handle()
    metadata_collection = db['image_metadata']  # Assuming the collection is named 'metadata'
    labels_collection = db['labels']  # Assuming the collection is named 'diagnosis_labels'
    
    # Building the initial match stage for the metadata
    match_stage = {'$match': {}}
    if age_range:
        match_stage['$match']['age_approx'] = {'$gte': age_range[0], '$lte': age_range[1]}
    if sex:
        match_stage['$match']['sex'] = sex
    if anatomical_sites:
        match_stage['$match']['anatom_site_general'] = {'$in': anatomical_sites}
    
    # Building the pipeline
    pipeline = [
        match_stage,
        {
            '$lookup': {
                'from': labels_collection.name,  # Refer to the labels collection
                'localField': 'image',  # The field from the metadata documents
                'foreignField': 'image',  # The field from the labels documents
                'as': 'diagnosis_labels'  # The output array field
            }
        },
        {'$unwind': '$diagnosis_labels'}  # Unwinding the diagnosis_labels array
    ]
    
    # If diagnosis codes are provided, we need to create an additional match stage
    if diagnosis_codes:
        # Each diagnosis code corresponds to a field name in the document, where the value is '1'
        diagnosis_match = {'$or': [{'diagnosis_labels.' + code: 1} for code in diagnosis_codes]}
        pipeline.append({'$match': diagnosis_match})
    
    # Execute the aggregation pipeline
    results = list(metadata_collection.aggregate(pipeline))
    
    for result in results:
        # Find the diagnosis code with a value of 1
        diagnosis_code = next((code for code, value in result['diagnosis_labels'].items() if value == 1), None)
        result['diagnosis_code'] = diagnosis_code

    return results