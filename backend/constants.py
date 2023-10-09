from pymongo import MongoClient
import os
from enum import Enum

# MongoDB connection settings
MONGODB_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'twitter_db'

DATA_LAKE_FOLDER = os.path.join(os.path.dirname(__file__), 'data.local')

class DataFolderNames(Enum):
    lda_topic_models = 'lda_topic_models'


class CollectionNames(Enum):
    internet_archive_urls = 'internet_archive_urls'
    original_tweets = 'original_tweets'
    analyzed_tweets = 'analyzed_tweets'
    tweet_text_original = 'tweet_text_original'
    tweet_spacy_match_original = 'tweet_spacy_match_original'
    tweet_translated = 'tweet_text_translated'
    tweet_spacy_match_in_english = 'tweet_spacy_match_in_english'
    tweet_processed = 'tweet_text_processed'
    tweet_sentiment = 'tweet_sentiment'
    topic_models_lda = 'topic_models_lda'
    tweet_topics_lda = 'tweet_topics_lda'
    tweet_topics_bertopic_arxiv = 'tweet_topics_bertopic_arxiv'
    tweet_topics_cardiffnlp = 'tweet_topics_cardiffnlp'
    user_location_translated = 'user_location_translated'
    user_location_coordinates = 'user_location_coordinates'
    user_location_country = 'user_location_country'
    user_demographics = 'user_demographics'
    user_demographics_result = 'user_demographics_result'
    user_m3_preprocessed = 'user_m3_preprocessed'



current_dir = os.path.dirname(os.path.abspath(__file__))
MONGODB_DATA_FOLDER = os.path.join(current_dir, 'mongodb_data')
if not os.path.exists(MONGODB_DATA_FOLDER):
    os.makedirs(MONGODB_DATA_FOLDER)

try:
    # Establish connection with MongoDB
    MONGODB_CLIENT = MongoClient(MONGODB_URI)
    
    DATABASE = MONGODB_CLIENT[DATABASE_NAME]
    
    # # create new collections if it doesn't exist
    # for collection_name in COLLECTION_NAME_REGISTRY.values():
    #     if collection_name not in DATABASE.list_collection_names():
    #         DATABASE.create_collection(collection_name)
    #         print(f'Created {collection_name}')    
    #     else:
    #         print(f'Collection {collection_name} already exists')    

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

    # Get database and collection
