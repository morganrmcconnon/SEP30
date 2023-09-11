from analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from analyze_tweets.translate_text import detect_and_translate_language
from analyze_tweets.sentiment_analysis import classify_sentiment
from analyze_tweets.topic_modelling import load_model, apply_lda, tokenize_lemmatize_and_remove_stopwords, topic_modelling
from analyze_tweets.detect_coordinates import detect_coordinates
from analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference
from analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon

import os
import json

GEOJSON_FILE = os.path.join(os.path.dirname(__file__), "data/countries.geojson")
GEOJSON_KEY_FOR_COUNTRY_NAME = 'ADMIN'

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
    sentiment_result, sentiment_confidence_probabilities = classify_sentiment(tweet_text_processed)

    # Topic modelling
    lda_topic_model = load_model(
        os.path.join(os.path.dirname(__file__), "topic_model/lda_model.model")
    )
    
    topics = apply_lda(tweet_text_processed, lda_topic_model)

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
    user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, id_key="id_str", name_key="name", screen_name_key="screen_name", description_key="description", lang_key="lang")

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
    country_name = detect_geojson_ploygon(latitude, longitude, geojson_file=GEOJSON_FILE, country_name_key=GEOJSON_KEY_FOR_COUNTRY_NAME) # The country name key is "ADMIN" in the geojson file
    
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


def analyze_multiple_tweet(tweet_objects, create_new_topic_model = False, topic_model_num_topics = 10):
    '''
    Analyze multiple tweet objects
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''

    new_tweet_objects = []

    for tweet_object in tweet_objects:

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

        # Text tokenized, lemmatized, and stemmed. You can change the tweet_text_in_english to just tweet_text if you want to keep the original language.
        tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(tweet_text_in_english)

        # Sentiment analysis
        sentiment_result, sentiment_confidence_probabilities = classify_sentiment(tweet_text_processed)

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
        lda_topic_model, topics_values = topic_modelling(tweets, num_topics = topic_model_num_topics)

    else:
        lda_topic_model = load_model(
            os.path.join(os.path.dirname(__file__), "topic_model/lda_model.model")
        )
        topics_values = json.load(open(os.path.join(os.path.dirname(__file__), "topic_model/topics_values.json"), "r"))
    
    for tweet in new_tweet_objects:
        # Topic modelling for each tweet
        tweet["text_analyzed"]['topics'] = apply_lda(tweet["text_analyzed"]["processed"], lda_topic_model)

    return new_tweet_objects


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
        latitude, longitude = detect_coordinates(location, language=location_lang_detected)

        # Detect polygon. This is to display the country name in the map.
        country_name = detect_geojson_ploygon(latitude, longitude, geojson_file=GEOJSON_FILE, country_name_key=GEOJSON_KEY_FOR_COUNTRY_NAME) # The country name key is "ADMIN" in the geojson file

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
    
        user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, id_key="id_str", name_key="name", screen_name_key="screen_name", description_key="description", lang_key="lang", use_translator_if_necessary = True)

        users_demographics_input.append(user_object_preprocessed)
    
    # Detect demographics using m3inference
    users_demographics = detect_demographics(users_demographics_input)

    # For each user object, store the demographics detection result
    for user_object in new_user_objects:
        user_object["demographics"] = users_demographics[user_object["id_str"]]

    return new_user_objects
