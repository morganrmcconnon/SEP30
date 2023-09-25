from flask import Flask, request, jsonify
from datetime import datetime
import time
import os
import json
from pymongo import MongoClient

from mongo_constants import DATABASE, CollectionNames

from services.analyze_tweets.sentiment_vader import check_sentiment
from services.analyze_tweets.sentiment_analysis import classify_sentiment
# from my_source import mySource
# from source import download_tweets_during_time_period, analyze_multiple_tweets, analyze_multiple_users, aggregate_tweet_objects_analysis_result, aggregate_user_objects_analysis_result

from get_analysis_result import get_analysis_result

try:
    # Try establishing connection with MongoDB
    MONGODB_CLIENT = MongoClient('mongodb://localhost:27017/')

    # Get database and collection

    # create a new database if it doesn't exist
    if 'twitter_db' not in MONGODB_CLIENT.list_database_names():
        DATABASE = MONGODB_CLIENT['twitter_db']
    else:
        DATABASE = MONGODB_CLIENT['twitter_db']

    # create new collections if it doesn't exist
    if 'original_tweets' not in DATABASE.list_collection_names():
        C_ORIGINAL_TWEETS = DATABASE.create_collection('original_tweets')
    else:
        C_ORIGINAL_TWEETS = DATABASE['original_tweets']

    if 'analyzed_tweets' not in DATABASE.list_collection_names():
        C_ANALYZED_TWEETS = DATABASE.create_collection('analyzed_tweets')
    else:
        C_ANALYZED_TWEETS = DATABASE['analyzed_tweets']

    if 'analyzed_users' not in DATABASE.list_collection_names():
        C_ANALYZED_USERS = DATABASE.create_collection('analyzed_users')
    else:
        C_ANALYZED_USERS = DATABASE['analyzed_users']
    
    _USING_DATABASE_ = True

except Exception as e:
    print('Failed to connect to MongoDB')
    print(e)
    _USING_DATABASE_ = False
        


CURRENT_DIR = os.path.dirname(__file__)
CACHE_FOLDER = os.path.join(CURRENT_DIR, "cache")
# A static folder for storing static files
CACHE_STATIC_FOLDER = os.path.join(CURRENT_DIR, "cache_static")
DB_FOLDER = os.path.join(CURRENT_DIR, "db_temp")
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)
if not os.path.exists(CACHE_STATIC_FOLDER):
    os.makedirs(CACHE_STATIC_FOLDER)
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
TOPIC_VALUES_FILE = os.path.join(CURRENT_DIR, "services/topic_model/topics.json")


app = Flask(__name__, static_folder=f"../frontend/dist", static_url_path="/")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/")
def hello_world():
    return "<p>Hello, there!</p>"


@app.route("/api/example_endpoint_get", methods=["GET"])
def endpoint_test_example_get_data():
    # Return content from server
    return {"greeting": "Hello!!!!!!"}


@app.route("/api/time")
@app.route("/backend/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/api/sentiment_vader", methods=["POST"])
def check_sentiment_with_vader():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    compound_score, sentiment_label = check_sentiment(text)
    return {"compound_score": compound_score, "sentiment_label": sentiment_label}


@app.route("/api/sentiment", methods=["POST"])
def check_sentiment_with_roberta():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    # Analyze the sentiment of text
    sentiment_result, confidence_probabilities = classify_sentiment(text=text)
    return {
        "sentiment_result": sentiment_result,
        "confidence_probabilities": confidence_probabilities,
    }


# @app.route("/api/test", methods=["GET"])
# def get_data_test():
#     # Return content from server
#     topics, sentiment_analysis_result = mySource()
#     topics = list(topics)
#     print(topics, sentiment_analysis_result)
#     return {"topics": topics, "negative tweets": sentiment_analysis_result[0],
#             "positive tweets": sentiment_analysis_result[1], "neutral tweets": sentiment_analysis_result[2]}


# frontend - toend: post
# backend - frontend: get -> return json REST API


# @app.route("/api/test")
# def get_data_test():
#     # Return content from server
#     topics, sentiment_analysis_result = mySource()
#     topics = list(topics)
#     print(topics, sentiment_analysis_result)
#     data = {"list1": topics, "list2": sentiment_analysis_result}
#     print(data)
#     return jsonify(data)


# @app.route("/api/analyze_multiple_tweet_full", methods=["GET"])
# @app.route("/backend/get_analyzed_data_full", methods=["GET"])
# def get_analyzed_data_full():

#     start_analysis_at = time.time()

#     all_downloaded_tweets_list = download_tweets_during_time_period(time_period=2)

#     if _USING_DATABASE_:
#         # Insert all downloaded tweets into MongoDB collection. Set id_str as the primary key - `_id`
#         # If the tweet with the same id_str already exists, do not insert it.
#         documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in all_downloaded_tweets_list if C_ORIGINAL_TWEETS.count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
#         if len(documents_to_insert) > 0:
#             db_op_result = C_ORIGINAL_TWEETS.insert_many(documents_to_insert)
#             print(f'Inserted {len(db_op_result.inserted_ids)} tweets')

#     with open(os.path.join(DB_FOLDER, "original_tweets.json"), "a") as json_file:
#         for tweet_object in all_downloaded_tweets_list:
#             json_file.write('\n' + json.dumps(tweet_object))

#     if _USING_DATABASE_:
#         # Get all cached tweet objects with id in all_downloaded_tweets_list in the collection
#         list_of_already_analyzed_tweets = list(C_ANALYZED_TWEETS.find({'_id': {'$in': [tweet_object['id_str'] for tweet_object in all_downloaded_tweets_list]}}))

#         # If a tweet with the same id_str already exists, do not analyze it.
#         list_of_tweets_to_analyze = [tweet_object for tweet_object in all_downloaded_tweets_list if C_ANALYZED_TWEETS.count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
        
#         # Analyze the tweet objects that are not cached
#         list_of_tweets_to_analyze, topics_values = analyze_multiple_tweets(list_of_tweets_to_analyze, filter_after_translating=True)

#         # Save analyzed tweets into MongoDB collection. Set id_str as the primary key - `_id`
#         # If the tweet with the same id_str already exists, do not insert it.
#         documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in list_of_tweets_to_analyze if C_ANALYZED_TWEETS.count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
#         if len(documents_to_insert) > 0:
#             db_op_result = C_ANALYZED_TWEETS.insert_many(documents_to_insert)
#             print(f'Saved {len(db_op_result.inserted_ids)} analyzed tweets')
    
#         # Merge the analyzed tweet objects with the cached tweet objects
#         all_downloaded_tweets_list = list_of_already_analyzed_tweets + list_of_tweets_to_analyze

#     else:
#         # Analyze all downloaded tweet objects
#         all_downloaded_tweets_list, topics_values = analyze_multiple_tweets(all_downloaded_tweets_list, filter_after_translating=True)

#     # cached_analysis_result = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_analysis_result.json"), "r"))

#     # all_downloaded_tweets_list = cached_analysis_result['tweet_objects']

#     # all_downloaded_tweets_list, topics_values = analyze_multiple_tweets(all_downloaded_tweets_list, filter_after_translating=True)
    
#     # analyzed_tweet_objects_list = [tweet_object for tweet_object in all_downloaded_tweets_list if tweet_object["text_analyzed"]["is_mental_health_related"]]

#     analyzed_tweet_objects_list = all_downloaded_tweets_list

#     with open(os.path.join(DB_FOLDER, "analyzed_tweets.json"), "a") as json_file:
#         for tweet_object in analyzed_tweet_objects_list:
#             json_file.write('\n' + json.dumps(tweet_object))


#     tweets_amount_info = {
#         "total_tweets_count": len(all_downloaded_tweets_list),
#         "mental_health_related_tweets_count": len(analyzed_tweet_objects_list)
#     }

#     complete_tweet_objects_analysis_at = time.time()

#     # Cache the analyzed tweet objects into a JSON file
#     with open(os.path.join(CACHE_FOLDER, "cache_tweets.json"), "w") as json_file:
#         json.dump({
#             "time": complete_tweet_objects_analysis_at, 
#             "tweet_objects": analyzed_tweet_objects_list
#         }, json_file)

#     # Analyze the users of the tweets

#     user_objects_list = [tweet_object["user"] for tweet_object in analyzed_tweet_objects_list]

#     if _USING_DATABASE_:

#         # Get all cached user objects with id in user_objects_list in the collection
#         list_of_already_analyzed_users = list(C_ANALYZED_USERS.find({'_id': {'$in': [user_object['id_str'] for user_object in user_objects_list]}}))

#         # If a user with the same id_str already exists, do not analyze it.
#         list_of_users_to_analyze = [user_object for user_object in user_objects_list if C_ANALYZED_USERS.count_documents({'_id': user_object["id_str"]}, limit = 1) == 0]

#         # Analyze the user objects that are not cached
#         if len(list_of_users_to_analyze) > 0:
#             list_of_users_to_analyze = analyze_multiple_users(list_of_users_to_analyze)

#         print(f'Analyzed {len(list_of_users_to_analyze)} users')

#         # Save analyzed users into MongoDB collection. Set id_str as the primary key - `_id`
#         # If the user with the same id_str already exists, do not insert it.
#         documents_to_insert = [{**user_object, '_id': user_object['id_str']} for user_object in list_of_users_to_analyze if C_ANALYZED_USERS.count_documents({'_id': user_object['id_str']}, limit = 1) == 0]
#         if len(documents_to_insert) > 0:
#             db_op_result = C_ANALYZED_USERS.insert_many(documents_to_insert)
#             print(f'Saved {len(db_op_result.inserted_ids)} analyzed users')

#         # Merge the analyzed user objects with the cached user objects
#         analyzed_user_objects_list = list_of_already_analyzed_users + list_of_users_to_analyze

#     else:
#         # Analyze all downloaded user objects
#         analyzed_user_objects_list = analyze_multiple_users(user_objects_list)

#     complete_user_objects_analysis_at = time.time()

#     with open(os.path.join(DB_FOLDER, "analyzed_users.json"), "a") as json_file:
#         for user_object in analyzed_user_objects_list:
#             json_file.write('\n' + json.dumps(user_object))


#     with open(os.path.join(CACHE_FOLDER, "cache_users.json"), "w") as json_file:
#         json.dump({
#             "time": complete_user_objects_analysis_at, 
#             "user_objects": analyzed_user_objects_list
#         }, json_file)

#     topics_count, sentiment_count, keywords_count, keywords_pairs = aggregate_tweet_objects_analysis_result(analyzed_tweet_objects_list)

#     complete_aggregating_tweet_objects_analysis_at = time.time()

#     # Cached the tweet_analyzed_result into a JSON file
#     with open(os.path.join(CACHE_FOLDER, "cache_tweet_analyzed_result.json"), "w") as json_file:
#         json.dump({
#             "time": complete_aggregating_tweet_objects_analysis_at,
#             "tweets_amount_info" : tweets_amount_info,
#             "sentiment_count" : sentiment_count,
#             "keywords_pairs": keywords_pairs,
#             "keywords_count" : keywords_count,
#             "topics_count" : topics_count,
#         }, json_file)

#     # Cached the tweets_amount_info into a JSON file
#     with open(os.path.join(CACHE_FOLDER, "cache_tweet_realtime.json"), "a") as json_file:
#         tweets_amount_info["analyzed_at"] = time.time()
#         json_file.write('\n' + json.dumps(tweets_amount_info))

#     countries_count, genders_count, age_groups_count, org_count = aggregate_user_objects_analysis_result(analyzed_user_objects_list)

#     complete_aggregating_user_objects_analysis_result_at = time.time()

#     with open(os.path.join(CACHE_FOLDER, "cache_user_analyzed_result.json"), "w") as json_file:
#         # Convert data to a JSON-formatted string and write it to the file
#         json.dump({
#             "time": complete_aggregating_user_objects_analysis_result_at,
#             "countries_count,": countries_count, 
#             "genders_count,": genders_count, 
#             "age_groups_count": age_groups_count,
#             "org_count": org_count,
#         } , json_file)

#     full_analysis_result = {
#         "analysis_timestamps": {
#             "start_analysis_at": start_analysis_at,
#             "complete_tweet_objects_analysis_at": complete_tweet_objects_analysis_at,
#             "complete_user_objects_analysis_at": complete_user_objects_analysis_at,
#             "complete_aggregating_tweet_objects_analysis_at": complete_aggregating_tweet_objects_analysis_at,
#             "complete_aggregating_user_objects_analysis_result_at": complete_aggregating_user_objects_analysis_result_at,
#             "end_analysis_at": time.time(),
#         },
#         "tweets_amount_info": tweets_amount_info,
#         "aggregated_result": {
#             "sentiment_count": sentiment_count,
#             "topics_count": topics_count,
#             "countries_count": countries_count,
#             "genders_count": genders_count,
#             "age_groups_count": age_groups_count,
#             "org_count": org_count,
#             "keywords_count": keywords_count,
#             "keywords_pairs": keywords_pairs,
#         },
#         "topics_values": topics_values,
#         "tweet_objects": analyzed_tweet_objects_list,
#         "user_objects": analyzed_user_objects_list,
#     }

#     # Cache the analyzed result into a JSON file
#     with open(os.path.join(CACHE_FOLDER, "cache_analysis_result.json"), "w") as json_file:
#         json.dump(full_analysis_result, json_file)
    
#     return full_analysis_result


@app.route("/api/analyze_multiple_tweet_cached")
@app.route("/backend/get_analyzed_data_cached", methods=["GET"])
def get_analyzed_data_cached():
    # Return cached analyzed result

    cached_analysis_result = json.load(open(os.path.join(CACHE_FOLDER, "cache_analysis_result.json"), "r"))

    return cached_analysis_result

@app.route("/api/analyze_multiple_tweet_cached_static")
@app.route("/backend/get_analyzed_data_cached_static", methods=["GET"])
@app.route("/backend/get_cached_static", methods=["GET"])
def get_analyzed_data_cached_static():
    # Return cached analyzed result from static folder

    cached_analysis_result = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_analysis_result.json"), "r"))

    return cached_analysis_result



@app.route("/api/analyze_multiple_tweet")
@app.route("/backend/get_analyzed_data", methods=["GET"])
def get_analyze_multiple_tweet_data():
    # Return content from server

    cached_analysis_result = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_analysis_result.json"), "r"))

    end_analysis_at = cached_analysis_result['analysis_timestamps']['end_analysis_at']

    print(end_analysis_at)

    # If the cached data is older than 10 minutes ago, re-analyze the tweets
    if time.time() - end_analysis_at > 6000:
        # return get_analyzed_data_full()
        return get_analyzed_data_cached()
        
    else:
        return get_analyzed_data_cached()

#Additional MongoDB functionalities
@app.route("/api/select_analyzed_tweets", methods=["GET"])
def select_analyzed_tweets():
    keyword = request.args.get('keyword')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Convert date strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Query MongoDB collection to select analyzed tweets based on keyword and date range
    selected_tweets = C_ANALYZED_TWEETS.find({
        'text': {'$regex': keyword, '$options': 'i'},  # Case-insensitive search
        'created_at': {'$gte': start_datetime, '$lte': end_datetime}
    })
    
    # Convert the MongoDB cursor to a list of dictionaries
    selected_tweets_list = list(selected_tweets)
    
    return jsonify(selected_tweets_list)

@app.route("/api/select_tweet_ids_by_date_range", methods=["GET"])
def select_tweet_ids_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Convert date strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Query MongoDB collection to select tweet IDs based on date range
    selected_tweet_ids = C_ANALYZED_TWEETS.find({
        'created_at': {'$gte': start_datetime, '$lte': end_datetime}
    }).distinct('id_str')  # Get distinct tweet IDs
    
    return jsonify(selected_tweet_ids)


@app.route("/api/select_tweets_by_timestamp_ms", methods=["GET"])
@app.route("/backend/select_tweets_by_timestamp_ms", methods=["GET"])
def select_tweets_by_timestamp_ms_range():
    start_timestamp_ms = request.args.get('start', type=str)
    end_timestamp_ms = request.args.get('end', type=str)
    default_timestamp_ms = str(int(datetime(year=2022, month=10, day=8, hour=12, minute=0).timestamp() * 1000))
    if start_timestamp_ms is None:
        start_timestamp_ms = default_timestamp_ms
    if end_timestamp_ms is None:
        end_timestamp_ms = default_timestamp_ms
    if (not start_timestamp_ms.isdigit()) or (not end_timestamp_ms.isdigit()):
        return jsonify([])
    if len(start_timestamp_ms) != 13 or len(end_timestamp_ms) != 13:
        return jsonify([])
    if start_timestamp_ms > end_timestamp_ms:
        return jsonify([])
    
    
    print(start_timestamp_ms, end_timestamp_ms)
    # Query MongoDB collection to select tweet IDs based on timestamp range
    # Join 2 collections, original_tweets and analyzed_tweets
    pipeline = [
        # find based on timestamp range
        {
            "$match": {
                "timestamp_ms": {"$gte": start_timestamp_ms, "$lte": end_timestamp_ms}
            }
        },
        # filter tweets that are not mental health related
        {
            "$match": {
                f"topic_bert_arxiv.id": 55 
            }
        },
    ]
    print("pipeline")
    print(pipeline)

    analysis_results = C_ANALYZED_TWEETS.aggregate(pipeline)
    
    return jsonify(analysis_results)


@app.route("/api/get_analyzed_data_by_tweet_ids", methods=["POST"])
def get_analyzed_data_by_tweet_ids():
    # Implement the logic to check if analysis results are cached for the given tweet IDs
    # If cached, retrieve and return the cached analysis results
    # If not cached, analyze the list of tweets and cache the results
    
    tweet_ids_to_analyze = request.json.get('tweet_ids')
    cached_analysis_results = []
    uncached_tweet_ids = []
    
    # Check which tweet IDs are already cached
    for tweet_id in tweet_ids_to_analyze:
        cached_result = C_ANALYZED_TWEETS.find_one({'_id': tweet_id})
        if cached_result:
            cached_analysis_results.append(cached_result)
        else:
            uncached_tweet_ids.append(tweet_id)
    
    # Analyze the uncached tweet IDs
    if uncached_tweet_ids:
        # Retrieve uncached tweets from MongoDB
        uncached_tweets = C_ORIGINAL_TWEETS.find({'id_str': {'$in': uncached_tweet_ids}})
        
        # DEBUG
        # For now, we will comment this out to save time when starting the Flask app. 
        # There is a possibility that we are not going to analyze tweets in the Flask backend.
        #  
        # Analyze the uncached tweets
        # analyzed_results = analyze_multiple_tweets(list(uncached_tweets), filter_after_translating=True)
        
        # # Cache the analyzed results in MongoDB
        # documents_to_insert = [{**result, '_id': result['id_str']} for result in analyzed_results]
        # if documents_to_insert:
        #     db_op_result = C_ANALYZED_TWEETS.insert_many(documents_to_insert)
        #     print(f'Saved {len(db_op_result.inserted_ids)} analyzed tweets')
        
        # cached_analysis_results.extend(analyzed_results)
    
    return jsonify(cached_analysis_results)
