from pymongo import MongoClient
from components.download_tweets.download_tweets import *
from components.download_tweets.get_download_url import *

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_db']
collection = db['original_tweets']

# Store tweets in MongoDB
def store_tweets_in_db(tweets):

    # Insert all tweets in MongoDB. Set id_str as the primary key - `_id`
    result = collection.insert_many([{**tweet, '_id': tweet['id_str']} for tweet in tweets])

    print(f'Inserted {len(result.inserted_ids)} tweets')

if __name__ == "__main__":
    # Get download url
    url = get_download_url(2011, 9, 27, 19, 48)
    print(url)
    # Download tweets
    tweets = download_tweets(url)
    # Store tweets in MongoDB
    store_tweets_in_db(tweets)