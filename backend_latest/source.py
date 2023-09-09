import json
import time
import os
from datetime import datetime, timedelta

from services.download_tweets.download_tweets import download_tweets
from services.download_tweets.get_download_url import get_download_url
from services.analyze_tweets.spacy_matcher import filter_tweet
from services.analyze_pipeline import analyze_multiple_tweet

#From analyze_pipeline.py
from services.analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from services.analyze_tweets.translate_text import detect_and_translate_language
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from services.analyze_tweets.topic_modelling import load_model, apply_lda, tokenize_lemmatize_and_remove_stopwords, \
    topic_modelling
from services.analyze_tweets.detect_coordinates import detect_coordinates
from services.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference
from services.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon

GEOJSON_FILE = os.path.join(os.path.dirname(__file__), "data\countries.geojson")
GEOJSON_KEY_FOR_COUNTRY_NAME = 'ADMIN'



#Merged analyze_multiple_tweet with analyze_multiple_tweets
def analyze_multiple_tweets(create_new_topic_model=False, topic_model_num_topics=10, period=5):
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
    data = filter_tweet(data)  # output is a list of dict
    tweets["mentalhealthtweets"] = len(data)

    # Analyze multiple tweet objects (code from analyze_multiple_tweet)
    new_tweet_objects = []

    for tweet_object in tweets:

        # Get the full, cleaned text of the tweet object
        tweet_text = clean_tweet_text(get_tweet_text(tweet_object))

        tweet_lang = tweet_object["lang"]

        if tweet_lang == "en":
            tweet_text_in_english = tweet_text
            tweet_lang_detected = "en"
        else:
            continue
            # Detect the language of the tweet and translate it to English
            tweet_text_in_english, tweet_lang_detected, _, _ = detect_and_translate_language(tweet_text)

        # If the user's language is not detected, set it to the detected tweet language [1]
        if tweet_object['user']['lang'] == None:
            tweet_object['user']['lang'] = tweet_lang_detected

        # Text tokenized, lemmatized, and stemmed. You can change the tweet_text_in_english to just tweet_text if you want to keep the original language.
        tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(tweet_text_in_english)

        # Sentiment analysis
        sentiment_result, sentiment_confidence_probabilities = classify_sentiment(
            tweet_text_in_english)  # tweet_text_processed

        new_tweet_objects.append(
            {
                **tweet_object,
                "text_analyzed": {
                    "original": tweet_text,
                    "in_english": tweet_text_in_english,
                    "lang_detected": tweet_lang_detected,
                    "processed": tweet_text_processed,
                    "sentiment": {
                        "result": sentiment_result,
                        "confidence_probabilities": sentiment_confidence_probabilities
                    },
                }
            }
        )

    # Topic modelling

    if create_new_topic_model:
        tweets = [tweet["text_analyzed"]["processed"] for tweet in new_tweet_objects]
        lda_topic_model, topics_values = topic_modelling(tweets, num_topics=topic_model_num_topics)

    else:
        lda_topic_model = load_model(
            os.path.join(os.path.dirname(__file__), "topic_model\lda_model.model")
        )
        topics_values = json.load(open(os.path.join(os.path.dirname(__file__), "topic_model\\topics.json"), "r"))

    for tweet in new_tweet_objects:
        # Topic modelling for each tweet
        tmp = apply_lda(tweet["text_analyzed"]["in_english"], lda_topic_model)
        topics = []
        for topic in tmp:
            topics.append([topic[0], float(topic[1])])
        tweet["text_analyzed"]['topics'] = topics

    return new_tweet_objects, tweets


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





#Code Merged from analyze_pipeline.py
def analyze_one_tweet(tweet_object):
    '''
    Analyze one tweet object
    
    The keys in the tweet object follows the Twitter API v1.1 dictionary.
    '''

    # Get the full, cleaned text of the tweet object
    tweet_text = clean_tweet_text(get_tweet_text(tweet_object))

    tweet_lang = tweet_object["lang"]

    if tweet_lang == "en":
        tweet_text_in_english = tweet_text
        tweet_lang_detected = "en"
    else:
        # Detect the language of the tweet and translate it to English
        tweet_text_in_english, tweet_lang_detected, _, _ = detect_and_translate_language(tweet_text)

    # If the user's language is not detected, set it to the detected tweet language [1]
    if tweet_object['user']['lang'] == None:
        tweet_object['user']['lang'] = tweet_lang_detected

    # Text tokenized, lemmatized, and stemmed
    tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(tweet_text_in_english)

    # Sentiment analysis
    sentiment_result, sentiment_confidence_probabilities = classify_sentiment(
        tweet_text_in_english)  # tweet_text_processed
    # print(sentiment_result, sentiment_confidence_probabilities, tweet_text_in_english)
    # Topic modelling
    lda_topic_model = load_model(
        os.path.join(os.path.dirname(__file__), "topic_model/lda_model.model")
    )

    topics = apply_lda(tweet_text_in_english, lda_topic_model)  # tweet_text_processed

    return {
        **tweet_object,
        "text_analyzed": {
            "original": tweet_text,
            "in_english": tweet_text_in_english,
            "lang_detected": tweet_lang_detected,
            "processed": tweet_text_processed,
            "sentiment": {
                "result": sentiment_result,
                "confidence_probabilities": sentiment_confidence_probabilities
            },
            "topics": topics
        },

    }


def analyze_one_user(user_object):
    '''
    Analyze one user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''
    # Preprocess user object for m3inference
    user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, id_key="id_str", name_key="name",
                                                                      screen_name_key="screen_name",
                                                                      description_key="description", lang_key="lang")

    # Detect demographics
    demographics = detect_demographics([user_object_preprocessed])

    # Get original location description
    location = user_object["location"]

    # Detect the language of the location description and translate it to English
    # Might be uneccessary if the user's lang is already defined
    location_in_english, location_lang_detected, _, _ = detect_and_translate_language(location)

    # If the language is not detected, set it to the detected location language, or the tweet's language (See [1] in this code file)
    if user_object['lang'] == None:
        user_object['lang'] = location_lang_detected

    # Detect coordinates
    latitude, longitude = detect_coordinates(location, language=location_lang_detected)

    # Detect polygon. This is to display the country name in the map.
    country_name = detect_geojson_ploygon(latitude, longitude, geojson_file=GEOJSON_FILE,
                                          country_name_key=GEOJSON_KEY_FOR_COUNTRY_NAME)  # The country name key is "ADMIN" in the geojson file

    return {
        **user_object,
        "demographics": demographics,
        "location_analyzed": {
            "in_english": location_in_english,
            "lang_detected": location_lang_detected,
            "latitude": latitude,
            "longitude": longitude,
            "country_name": country_name
        }
    }



def analyze_multiple_user(user_objects):
    '''
    Analyze multiple user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''

    new_user_objects = []

    for user_object in user_objects:

        # Get original location description
        location = user_object["location"]

        # Detect the language of the location description and translate it to English
        # Might be uneccessary if the user's lang is already defined
        location_in_english, location_lang_detected, _, _ = detect_and_translate_language(location)

        # If the language is not detected, set it to the detected location language, or the tweet's language (See [1] in this code file)
        if user_object['lang'] == None:
            user_object['lang'] = location_lang_detected

        # Detect coordinates
        print(user_object)
        coordinates = detect_coordinates(location, language=location_lang_detected)

        if coordinates == None:
            continue

        latitude, longitude = coordinates[0], coordinates[1]

        # Detect polygon. This is to display the country name in the map.
        country_name = detect_geojson_ploygon(latitude, longitude, geojson_file=GEOJSON_FILE, country_name_key_in_properties=GEOJSON_KEY_FOR_COUNTRY_NAME)  # The country name key is "ADMIN" in the geojson file

        new_user_objects.append(
            {
                **user_object,
                "location_analyzed": {
                    "in_english": location_in_english,
                    "lang_detected": location_lang_detected,
                    "latitude": latitude,
                    "longitude": longitude,
                    "country_name": country_name
                }
            }
        )

    users_demographics_input = []

    # Preprocess user object for m3inference
    for user_object in new_user_objects:
        user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, id_key="id_str", name_key="name",
                                                                          screen_name_key="screen_name",
                                                                          description_key="description",
                                                                          lang_key="lang",
                                                                          use_translator_if_necessary=True)

        users_demographics_input.append(user_object_preprocessed)

    # Detect demographics using m3inference
    users_demographics = detect_demographics(users_demographics_input)

    # For each user object, store the demographics detection result
    for user_object in new_user_objects:
        user_object["demographics"] = users_demographics[user_object["id_str"]]

    return new_user_objects
