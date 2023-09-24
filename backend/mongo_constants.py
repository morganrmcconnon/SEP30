from pymongo import MongoClient
import os
from enum import Enum

# MongoDB connection settings
MONGODB_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'twitter_db'


# class syntax
class CollectionNames(Enum):
    internet_archive_urls = 'internet_archive_urls'
    original_tweets = 'original_tweets'
    analyzed_tweets = 'analyzed_tweets'
    tweet_text_original = 'analysis_tweet_text_original'
    tweet_filtered_pre_translation = 'analysis_tweet_filtered_pre_translation'
    tweet_translated = 'analysis_tweet_translated'
    tweet_filtered_post_translation = 'analysis_tweet_filtered_post_translation'
    tweet_processed = 'analysis_tweet_text_processed'
    tweet_sentiment = 'analysis_tweet_sentiment'
    tweet_topics_lda = 'analysis_tweet_topics_lda'
    tweet_topics_lda_results = 'analysis_tweet_topics_lda_results'
    tweet_topics_bertopic_arxiv = 'analysis_tweet_topics_bertopic_arxiv'
    tweet_topics_cardiffnlp = 'analysis_tweet_topics_cardiffnlp'
    user_location_translated = 'analysis_user_location_translated'
    user_location_coordinates = 'analysis_user_location_coordinates'
    user_location_country = 'analysis_user_location_country'
    user_demographics = 'analysis_user_demographics'
    user_demographics_result = 'analysis_user_demographics_result'
    user_m3_preprocessed = 'analysis_user_m3_preprocessed'



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
