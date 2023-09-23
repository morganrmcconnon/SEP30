import os
import json

if __name__ == '__main__':

    from mongo_constants import DATABASE, DATABASE_NAME, MONGODB_DATA_FOLDER

    # Function to import a JSON file into a collection
    def import_json_file(collection_name, json_file_path):
        
        collection = DATABASE[collection_name]
        
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            collection.insert_many(data)
            print(f"Imported {len(data)} documents into the '{collection_name}' collection")
    

    # Iterate through the JSON files in the input directory and import them
    for root, _, files in os.walk(MONGODB_DATA_FOLDER):
        for file in files:
            if file.endswith(".json"):
                collection_name = os.path.splitext(file)[0]  # Use the file name as the collection name
                json_file_path = os.path.join(root, file)
                import_json_file(collection_name, json_file_path)

    print(f"Imported JSON files from '{MONGODB_DATA_FOLDER}' into the '{DATABASE_NAME}' database.")
