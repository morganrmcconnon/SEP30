from flask import Flask, request, jsonify
import time
import os
import json

from services.analyze_tweets.sentiment_vader import check_sentiment
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from my_source import mySource
from source import download_tweets_during_time_period, analyze_multiple_tweets, analyze_multiple_users, aggregate_tweet_objects_analysis_result, aggregate_user_objects_analysis_result

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


@app.route("/api/test")
def get_data_test():
    # Return content from server
    topics, sentiment_analysis_result = mySource()
    topics = list(topics)
    print(topics, sentiment_analysis_result)
    data = {"list1": topics, "list2": sentiment_analysis_result}
    print(data)
    return jsonify(data)


@app.route("/api/analyze_multiple_tweet_full", methods=["GET"])
@app.route("/backend/get_analyzed_data_full", methods=["GET"])
def get_analyzed_data_full():

    start_analysis_at = time.time()

    all_downloaded_tweets_list = download_tweets_during_time_period()

    # store_tweets_in_db
    with open(os.path.join(DB_FOLDER, "original_tweets.json"), "a") as json_file:
        for tweet_object in all_downloaded_tweets_list:
            json_file.write('\n' + json.dumps(tweet_object))

    analyzed_tweet_objects_list, topics_values = analyze_multiple_tweets(all_downloaded_tweets_list, filter_after_translating=True)

    # store_tweets_in_db
    with open(os.path.join(DB_FOLDER, "analyzed_tweets.json"), "a") as json_file:
        for tweet_object in analyzed_tweet_objects_list:
            json_file.write('\n' + json.dumps(tweet_object))


    tweets_amount_info = {
        "total_tweets_count": len(all_downloaded_tweets_list),
        "mental_health_related_tweets_count": len(analyzed_tweet_objects_list)
    }

    complete_tweet_objects_analysis_at = time.time()

    # Cache the analyzed tweet objects into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_tweets.json"), "w") as json_file:
        json.dump({
            "time": complete_tweet_objects_analysis_at, 
            "tweet_objects": analyzed_tweet_objects_list
        }, json_file)

    # Analyze the users of the tweets

    user_objects_list = [tweet_object["user"] for tweet_object in analyzed_tweet_objects_list]

    analyzed_user_objects_list = analyze_multiple_users(user_objects_list)

    complete_user_objects_analysis_at = time.time()

    
    # store_tweets_in_db
    with open(os.path.join(DB_FOLDER, "analyzed_users.json"), "a") as json_file:
        for user_object in analyzed_user_objects_list:
            json_file.write('\n' + json.dumps(user_object))


    with open(os.path.join(CACHE_FOLDER, "cache_users.json"), "w") as json_file:
        json.dump({
            "time": complete_user_objects_analysis_at, 
            "user_objects": analyzed_user_objects_list
        }, json_file)

    topics_count, sentiment_count, keywords_count, keywords_pairs = aggregate_tweet_objects_analysis_result(analyzed_tweet_objects_list)

    complete_aggregating_tweet_objects_analysis_at = time.time()

    # Cached the tweet_analyzed_result into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_tweet_analyzed_result.json"), "w") as json_file:
        json.dump({
            "time": complete_aggregating_tweet_objects_analysis_at,
            "tweets_amount_info" : tweets_amount_info,
            "sentiment_count" : sentiment_count,
            "keywords_pairs": keywords_pairs,
            "keywords_count" : keywords_count,
            "topics_count" : topics_count,
        }, json_file)

    # Cached the tweets_amount_info into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_tweet_realtime.json"), "a") as json_file:
        tweets_amount_info["analyzed_at"] = time.time()
        json_file.write('\n' + json.dumps(tweets_amount_info))

    countries_count, genders_count, age_groups_count = aggregate_user_objects_analysis_result(analyzed_user_objects_list)

    complete_aggregating_user_objects_analysis_result_at = time.time()

    with open(os.path.join(CACHE_FOLDER, "cache_user_analyzed_result.json"), "w") as json_file:
        # Convert data to a JSON-formatted string and write it to the file
        json.dump({
            "time": complete_aggregating_user_objects_analysis_result_at,
            "countries_count,": countries_count, 
            "genders_count,": genders_count, 
            "age_groups_count": age_groups_count,
        } , json_file)

    full_analysis_result = {
        "analysis_timestamps": {
            "start_analysis_at": start_analysis_at,
            "complete_tweet_objects_analysis_at": complete_tweet_objects_analysis_at,
            "complete_user_objects_analysis_at": complete_user_objects_analysis_at,
            "complete_aggregating_tweet_objects_analysis_at": complete_aggregating_tweet_objects_analysis_at,
            "complete_aggregating_user_objects_analysis_result_at": complete_aggregating_user_objects_analysis_result_at,
            "end_analysis_at": time.time(),
        },
        "tweets_amount_info": tweets_amount_info,
        "aggregated_result": {
            "sentiment_count": sentiment_count,
            "topics_count": topics_count,
            "countries_count": countries_count,
            "genders_count": genders_count,
            "age_groups_count": age_groups_count,
            "keywords_count": keywords_count,
            "keywords_pairs": keywords_pairs,
        },
        "topics_values": topics_values,
        "tweet_objects": analyzed_tweet_objects_list,
        "user_objects": analyzed_user_objects_list,
    }

    # Cache the analyzed result into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_analysis_result.json"), "w") as json_file:
        json.dump(full_analysis_result, json_file)
    
    return full_analysis_result


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
        return get_analyzed_data_full()
        
    else:
        return get_analyzed_data_cached()