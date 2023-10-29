from pymongo import MongoClient

# Connecting to the MongoDB server (change the connection string as needed)
client = MongoClient('mongodb://root:mysecretpassword@localhost:27017/')

# 1. List All Databases
databases = client.list_database_names()
print("Databases:", databases)
print()

# Looping through each database
for db_name in databases:
    db = client[db_name]
    
    # 2. List All Collections in a Database
    collections = db.list_collection_names()
    print("Collections in database '{}':".format(db_name), collections)
    print()
    
    # Looping through each collection
    for collection_name in collections:
        collection = db[collection_name]
        
        # 3. Get Count of Documents in a Collection
        count_documents = collection.count_documents({})
        print("Number of documents in collection '{}':".format(collection_name), count_documents)
        
        # 4. Print a Few Documents from a Collection
        print("Some documents from '{}':".format(collection_name))
        for doc in collection.find().limit(5):
            print(doc)
        print()
        
        # 5. Get Information About Indexes
        indexes = collection.index_information()
        print("Indexes on collection '{}':".format(collection_name), indexes)
        print()
        
        # 6. Get Collection Stats
        stats = db.command("collstats", collection_name)
        print("Stats for collection '{}':".format(collection_name), stats)
        print()
        
        # 7. Check Disk Space Used by a Database (This is reported at the database level)
        if collection_name == collections[0]:  # Only print database stats once
            db_stats = db.command("dbstats")
            print("Disk space used by database '{}':".format(db_name), db_stats['dataSize'], "bytes")
            print()

print("Overview completed.")
