from workflow import *
import json
from services.analyze_pipeline import *
from datetime import datetime, timedelta
from services.download_tweets.download_tweets import *
from services.download_tweets.get_download_url import *
import time

def mySource():
    # data = download_tweets(0)
    # return {2,3}, [2,3,1]
    data = []

    file_path = "data\\test.json"  # Replace with the actual path to your file
    with open(file_path, "r") as json_file:
        for line in json_file:
            data.append((json.loads(line)))

    data = filter_tweets(data)  # output is a list of dict

    # this file will contain all data fields of interest
    filtered_data_full_tweets = save_data_full('data\\full_0.json', data)

    # this file will contain tweets only which have been translated
    data = save_complete_data('data\\data.json', filtered_data_full_tweets)

    print(data)

    tweet_data = []
    for text in data:
        tweet_data.append(text["text_original"])

    keywords = topic_modelling(tweet_data)

    topics = topic_modelling_define_topics(keywords)

    sentiment_analysis_result = sentiment_analysis(tweet_data)

    # location_data = save_extracted_location_data('data\\location.json', data)

    # age_data = save_extracted_age('data\\age.json', location_data)

    return topics, sentiment_analysis_result


def analyze_multiple_tweets(period = 5):
    data = []

    tweets = {
        "total": 0,
        "mentalhealthtweets": 0
    }

    # Get the current date and time
    current_datetime = datetime.now()
    previous_minute = current_datetime - timedelta(minutes=60)

    # Extract the day and month from the current date
    current_day, current_month, current_hour, current_minute = current_datetime.day, current_datetime.month, current_datetime.hour, current_datetime.minute

    current_year = 2022

    for i in range(period):
        # Get download url
        current_minute -= 1

        if current_minute == -1:
            current_minute = 59
            current_year, current_month, current_day, current_hour = previous_minute.year, previous_minute.month, previous_minute.day, previous_minute.hour
            current_year = 2022

        print(current_year, current_month, current_day, current_hour, current_minute)
        url = get_download_url(current_year, current_month, current_day, current_hour, current_minute)
        print(url)
        # Download tweets
        data.extend(download_tweets(url))

    #file_path = "data\\test.json"  # Replace with the actual path to your file
    #with open(file_path, "r") as json_file:
        #for line in json_file:
            #data.append((json.loads(line)))

    tweets["total"] = len(data)
    data = filter_tweets(data)  # output is a list of dict
    tweets["mentalhealthtweets"] = len(data)

    return analyze_multiple_tweet(data), tweets


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

    # Open the JSON file in write mode
    with open(os.path.join(os.path.dirname(__file__), "data\\cache_tweets.json"), "w") as json_file:
        # Convert data to a JSON-formatted string and write it to the file
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
        sentiment_analysis_result[sentiment_result] += 1
        # ---------sentiment processing----------#

    tweet_analyzed_result = [{
        "time": time.time()
    }, sentiment_analysis_result
        , topics
        , tweets]

    with open(os.path.join(os.path.dirname(__file__), "data\\cache_tweet_analyzed_result.json"), "w") as json_file:
        # Convert data to a JSON-formatted string and write it to the file
        json.dump(tweet_analyzed_result, json_file)

    with open(os.path.join(os.path.dirname(__file__), "data\\cache_tweet_realtime.json"), "a") as json_file:
        tweets["analyzed_at"] = time.time()
        # Convert data to a JSON-formatted string and write it to the file
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

    with open(os.path.join(os.path.dirname(__file__), "data\\cache_users.json"), "w") as json_file:
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

    with open(os.path.join(os.path.dirname(__file__), "data\\cache_user_analyzed_result.json"), "w") as json_file:
        # Convert data to a JSON-formatted string and write it to the file
        json.dump(user_analyzed_result, json_file)

    return country_names, genders , ages