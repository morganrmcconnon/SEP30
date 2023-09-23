from pymongo import MongoClient
import os

# MongoDB connection settings
MONGODB_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'twitter_db'

COLLECTIONS_LIST = [ 
    'original_tweets',
    'internet_archive_urls',
    'tweet_translated',
    'tweet_filtered_pre_translation',
    'tweet_filtered_post_translation',
    'tweet_processed',
    'tweet_sentiment',
    'tweet_topics_lda',
    'tweet_topics_lda_results',
    'tweet_topics_bertopic_arxiv',
    'tweet_topics_cardiffnlp',
    'user_location_translated',
    'user_location_coordinates',
    'user_m3_preprocessed',
    'user_demographics'
]

current_dir = os.path.dirname(os.path.abspath(__file__))
MONGODB_DATA_FOLDER = os.path.join(current_dir, 'mongodb_data')
if not os.path.exists(MONGODB_DATA_FOLDER):
    os.makedirs(MONGODB_DATA_FOLDER)

try:
    # Establish connection with MongoDB
    MONGODB_CLIENT = MongoClient(MONGODB_URI)
    
    # create a new database if it doesn't exist
    if DATABASE_NAME not in MONGODB_CLIENT.list_database_names():
        DATABASE = MONGODB_CLIENT[DATABASE_NAME]
    else:
        DATABASE = MONGODB_CLIENT[DATABASE_NAME]

    # create new collections if it doesn't exist
    for collection_name in COLLECTIONS_LIST:
        if collection_name not in DATABASE.list_collection_names():
            DATABASE.create_collection(collection_name)
            print(f'Created {collection_name}')    
        else:
            print(f'Collection {collection_name} already exists')    


    
    DATABASE = MONGODB_CLIENT[DATABASE_NAME]

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

    # Get database and collection
