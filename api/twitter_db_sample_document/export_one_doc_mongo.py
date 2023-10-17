import pymongo
import json

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if needed
db = client["twitter_db"]

# Get a list of all collections in the database
collections = db.list_collection_names()

# Export a single document from each collection
for collection_name in collections:
    collection = db[collection_name]
    document = collection.find_one()

    # Convert ObjectId to str for serialization
    if document:
        document["_id"] = str(document["_id"])

        with open(f"{collection_name}.json", "w") as outfile:
            json.dump(document, outfile)

# Close the MongoDB connection
client.close()
