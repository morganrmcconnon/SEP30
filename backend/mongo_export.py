import os
import json

if __name__ == '__main__':

    from mongo_constants import DATABASE, MONGODB_DATA_FOLDER

    # Function to export a collection to a JSON file
    def export_collection_to_json(collection_name):
        collection = DATABASE[collection_name]
        documents = list(collection.find({}))
        
        # Define the output JSON file path
        output_file = os.path.join(MONGODB_DATA_FOLDER, f"{collection_name}.json")
        
        # Export documents to JSON file
        with open(output_file, 'w') as json_file:
            json.dump(documents, json_file, default=str)


    # Get a list of collection names in the database
    collection_names = DATABASE.list_collection_names()

    # Export each collection to a JSON file
    for collection_name in collection_names:
        export_collection_to_json(collection_name)

    print(f"Exported {len(collection_names)} collections to JSON files in '{MONGODB_DATA_FOLDER}'")
