from flask import Flask, request, jsonify
import time
import os
import json
from services.analyze_tweets.sentiment_vader import check_sentiment
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from source import analyze_multiple_user
from my_source import mySource
from source import analyze_multiple_tweets

CURRENT_DIR = os.path.dirname(__file__)
CACHE_FOLDER = os.path.join(CURRENT_DIR, "cache")
# A static folder for storing static files
CACHE_STATIC_FOLDER = os.path.join(CURRENT_DIR, "cache_static") 
TOPIC_VALUES_FILE = os.path.join(CURRENT_DIR, "services/topic_model/topics.json")


app = Flask(__name__, static_folder=f"../frontend/dist", static_url_path="/")


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/api/")
def hello_world():
    return "<p>Hello, there!</p>"


@app.route("/api/example_endpoint_test", methods=["GET"])
def endpoint_test_example_get_data():
    # Return content from server
    return {"greeting": "Hello!!!!!!"}


@app.route("/api/time")
def get_current_time():
    return {'time': time.time()}


@app.route("/api/sentiment_vader", methods=["POST"])
def check_sentiment_with_vader():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    compound_score, sentiment_label = check_sentiment(text)
    return {'compound_score': compound_score, 'sentiment_label': sentiment_label}


@app.route("/api/sentiment", methods=["POST"])
def check_sentiment_with_roberta():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    # Analyze the sentiment of text
    sentiment_result, confidence_probabilities = classify_sentiment(text=text)
    return {'sentiment_result': sentiment_result, 'confidence_probabilities': confidence_probabilities}


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
    data = {
        'list1': topics,
        'list2': sentiment_analysis_result
    }
    print(data)
    return jsonify(data)



@app.route("/api/analyze_multiple_tweet_full", methods=["GET"])
def get_analyzed_data_full():
    # Analyze multiple tweets and return the unformatted result 

    tweet_objects_list, tweets_info, topics_values = analyze_multiple_tweets()

    #store_tweets_in_db(tweet_objects_list)

    user_objects_list = [tweet_object["user"] for tweet_object in tweet_objects_list]

    user_objects_list = analyze_multiple_user(user_objects_list)

    return jsonify({
        'tweets_info': tweets_info,
        'tweets': tweet_objects_list,
        'users': user_objects_list,
        'topics': topics_values,
    })



def wrap_tweet_analyzed_result(data, tweets):
    sentiment_analysis_result = {
        "negative": 0,
        "positive": 0,
        "neutral": 0
    }

    topics = {}
    for i in range(5):
        topics[i] = 0

    data = [{
        "time": time.time()
    }, data]
    # Data to write to the JSON file

    # print(data)

    # Cached the analyzed result into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_tweets.json"), "w") as json_file:
        json.dump(data, json_file)

    for tweet_object in data[1]:
        # print(tweet_object)
        text_analyzed_result = tweet_object["text_analyzed"]

        # ---------topic processing----------#
        topic = text_analyzed_result["topics"]
        highest_score_topic = max(topic, key=lambda x: x[1])
        topics[highest_score_topic[0]] += 1
        # ---------topic processing----------#

        # ---------sentiment processing----------#
        sentiment_result = text_analyzed_result["sentiment"]["result"]
        if sentiment_result not in sentiment_analysis_result:
            sentiment_analysis_result[sentiment_result] = 1
        else:
            sentiment_analysis_result[sentiment_result] += 1
        # ---------sentiment processing----------#

    tweet_analyzed_result = [{
        "time": time.time()
    }, sentiment_analysis_result
        , topics
        , tweets]

    # Cached the analyzed result into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_tweet_analyzed_result.json"), "w") as json_file:
        json.dump(tweet_analyzed_result, json_file)

    # Cached the analyzed result into a JSON file
    with open(os.path.join(CACHE_FOLDER, "cache_tweet_realtime.json"), "a") as json_file:
        tweets["analyzed_at"] = time.time()
        json.dump(tweets, json_file)
        json.dump('\n', json_file)

    return topics, sentiment_analysis_result


def wrap_user_analyzed_result(data):

    country_names = {}

    genders = {
        "female":0,
        "male":0
    }

    ages = {
        '19-29': 0,
        '30-39': 0,
        '<=18': 0,
        '>=40': 0
    }

    with open(os.path.join(CACHE_FOLDER, "cache_users.json"), "w") as json_file:
        # Convert data to a JSON-formatted string and write it to the file
        json.dump([{ "time": time.time()}, data] , json_file)

    for user_object in data:
        #print(user_object)

        # ---------location processing----------#
        country_name = user_object["location_analyzed"]["country_name"]
        country_names[country_name] = country_names.get(country_name, 0) + 1
        # ---------location processing----------#

        # ---------gender processing----------#
        gender_scores = user_object["demographics"]["gender"]
        gender = max(gender_scores, key=gender_scores.get)
        genders[gender] += 1

        # ---------age processing----------#
        age_scores = user_object["demographics"]["age"]
        age = max(age_scores, key=age_scores.get)
        ages[age] += 1

    user_analyzed_result = [{
        "time": time.time()
    }, country_names
        , genders
        , ages]

    with open(os.path.join(CACHE_FOLDER, "cache_user_analyzed_result.json"), "w") as json_file:
        # Convert data to a JSON-formatted string and write it to the file
        json.dump(user_analyzed_result, json_file)

    return country_names, genders , ages



@app.route("/api/analyze_multiple_tweet")
def get_data_test_2():
    # Return content from server

    tweet_objects_list = json.load(open(os.path.join(CACHE_FOLDER, "cache_tweet_analyzed_result.json"), "r"))

    get_writing_time = tweet_objects_list[0]["time"]

    sentiment_analysis_result, tweets_amount_info, topics = {}, {}, {}

    for i in range(5):
        topics[i] = 0

    if (time.time() - get_writing_time > 6000):
        tweet_objects_list, tweets_amount_info, topics_values = analyze_multiple_tweets()

        #store_tweets_in_db(data)

        user_objects_list = [tweet_object["user"] for tweet_object in tweet_objects_list]

        user_objects_list = analyze_multiple_user(user_objects_list)

        topics, sentiment_analysis_result = wrap_tweet_analyzed_result(tweet_objects_list, tweets_amount_info)

        country_names, genders, ages = wrap_user_analyzed_result(user_objects_list)
    else:
        sentiment_analysis_result = tweet_objects_list[1]
        topics = tweet_objects_list[2]
        tweets_amount_info = tweet_objects_list[3]
        tweet_objects_list = json.load(open(os.path.join(CACHE_FOLDER, "cache_user_analyzed_result.json"), "r"))
        country_names, genders, ages = tweet_objects_list[1], tweet_objects_list[2], tweet_objects_list[3]
        topics_values = json.load(open(TOPIC_VALUES_FILE, "r"))

    return jsonify(topics, sentiment_analysis_result, tweets_amount_info,  country_names, genders, ages, topics_values)



@app.route("/api/analyze_multiple_tweet_cached")
def get_data_test_cached():
    # Return cached analyzed result

    data = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_tweet_analyzed_result.json"), "r"))

    sentiment_analysis_result, tweets, topics = {}, {}, {}

    sentiment_analysis_result = data[1]

    topics = data[2]

    tweets = data[3]

    data = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_user_analyzed_result.json"), "r"))

    country_names, genders, ages = data[1], data[2], data[3]

    topics_values = json.load(open(TOPIC_VALUES_FILE, "r"))

    return jsonify(topics, sentiment_analysis_result, tweets,  country_names, genders, ages, topics_values)