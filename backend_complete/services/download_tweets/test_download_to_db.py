from pymongo import MongoClient
from download_tweets import download_tweets
from get_download_url import get_download_url

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_db']
collection = db['original_tweets']

# Store tweets in MongoDB
def store_tweets_in_db(tweets):
    for tweet_json_object in tweets:
        result = collection.insert_one(tweet_json_object)
        print('One tweet: {0}'.format(result.inserted_id))


if __name__ == "__main__":
    # Get download url
    url = get_download_url(2022, 11, 1, 0, 0)
    # Download tweets
    tweets = download_tweets(url)
    # Store tweets in MongoDB
    store_tweets_in_db(tweets)