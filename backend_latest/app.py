from flask import Flask, request, jsonify
import time
import os
import json
from services.analyze_tweets.sentiment_vader import check_sentiment
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from services.analyze_pipeline import analyze_multiple_user
from my_source import mySource
from source import wrap_tweet_analyzed_result, wrap_user_analyzed_result, analyze_multiple_tweets

# from flask_vite import Vite

# # Get and set directory for static files (ie. index.html, css, and bundled JS)
# # defaults to 'dist', the default name of Parcel's build directory
# build_dir = os.getenv("BUILD_DIR", "dist")
# print("Build dir:", build_dir)

# app = Flask(__name__, static_folder=f"../{build_dir}", static_url_path="/")

app = Flask(__name__)


# vite = Vite(app)

# # or
# vite = Vite()
# vite.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, there!</p>"


@app.route("/data", methods=["GET"])
def get_data():
    # Return content from server
    return {"greeting": "Hello!!!!!!"}


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route("/sentiment_vader", methods=["POST"])
def check_sentiment_with_vader():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    compound_score, sentiment_label = check_sentiment(text)
    return {'compound_score': compound_score, 'sentiment_label': sentiment_label}


@app.route("/sentiment", methods=["POST"])
def check_sentiment_with_roberta():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    # Analyze the sentiment of text
    sentiment_result, confidence_probabilities = classify_sentiment(text=text)
    return {'sentiment_result': sentiment_result, 'confidence_probabilities': confidence_probabilities}


# @app.route("/test", methods=["GET"])
# def get_data_test():
#     # Return content from server
#     topics, sentiment_analysis_result = mySource()
#     topics = list(topics)
#     print(topics, sentiment_analysis_result)
#     return {"topics": topics, "negative tweets": sentiment_analysis_result[0],
#             "positive tweets": sentiment_analysis_result[1], "neutral tweets": sentiment_analysis_result[2]}


# frontend - toend: post
# backend - frontend: get -> return json REST API

@app.route("/test")
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


@app.route("/analyze_multiple_tweet")
def get_data_test_2():
    # Return content from server

    data = json.load(open(os.path.join(os.path.dirname(__file__), "data\\cache_tweet_analyzed_result.json"), "r"))

    get_writing_time = data[0]["time"]

    sentiment_analysis_result, tweets, topics = {}, {}, {}

    for i in range(5):
        topics[i] = 0

    if (time.time() - get_writing_time > 6000):
        data, tweets = analyze_multiple_tweets()

        #store_tweets_in_db(data)

        user_data = []

        for line in data:
            user_data.append(line["user"])

        user_data = analyze_multiple_user(user_data)

        topics, sentiment_analysis_result = wrap_tweet_analyzed_result(data, tweets)

        country_names, genders, ages = wrap_user_analyzed_result(user_data)
    else:
        sentiment_analysis_result = data[1]
        topics = data[2]
        tweets = data[3]
        data = json.load(open(os.path.join(os.path.dirname(__file__), "data\\cache_user_analyzed_result.json"), "r"))
        country_names, genders, ages = data[1], data[2], data[3]

    return jsonify(topics, sentiment_analysis_result, tweets,  country_names, genders, ages)



@app.route("/analyze_multiple_tweet_full", methods=["GET"])
def get_data_test_3():
    # Return content from server

    tweets, topics = {}, {}

    for i in range(5):
        topics[i] = 0

    data, tweets = analyze_multiple_tweets()

    #store_tweets_in_db(data)

    user_data = []

    for line in data:
        user_data.append(line["user"])

    user_data = analyze_multiple_user(user_data)

    return jsonify(data, tweets, user_data)
