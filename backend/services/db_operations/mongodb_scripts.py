from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_db']
collection = db['original_tweets']

# Store tweets in MongoDB
def store_tweets_in_db(tweets):
    for tweet_json_object in tweets:
        collection.insert_one(tweet_json_object)


# Example scripts for querying tweets from MongoDB

def select_tweets_by_daterange(start_timestamp_ms, end_timestamp_ms):
    return collection.find({'timestamp_ms': {'$gte': start_timestamp_ms, '$lt': end_timestamp_ms}})

def select_tweets_by_daterange_and_one_keyword(start_timestamp_ms, end_timestamp_ms, keyword):
    return collection.find({'$and': [{'timestamp_ms': {'$gte': start_timestamp_ms, '$lt': end_timestamp_ms}}, {'$text': {'$search': keyword}}]})

def select_tweets_by_daterange_and_multiple_keywords(start_timestamp_ms, end_timestamp_ms, keywords):
    return collection.find({'$and': [{'timestamp_ms': {'$gte': start_timestamp_ms, '$lt': end_timestamp_ms}}, {'$text': {'$search': keywords}}]})

def select_tweets_by_daterange_and_one_keyword_and_one_language(start_timestamp_ms, end_timestamp_ms, keyword, language):
    return collection.find({'$and': [{'timestamp_ms': {'$gte': start_timestamp_ms, '$lt': end_timestamp_ms}}, {'$text': {'$search': keyword}}, {'lang': language}]})

def select_tweets_by_daterange_and_multiple_keywords_and_one_language(start_timestamp_ms, end_timestamp_ms, keywords, language):
    return collection.find({'$and': [{'timestamp_ms': {'$gte': start_timestamp_ms, '$lt': end_timestamp_ms}}, {'$text': {'$search': keywords}}, {'lang': language}]})