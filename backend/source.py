import json
import os
from datetime import datetime, timedelta

from services.download_tweets.download_tweets import download_tweets
from services.download_tweets.get_download_url import get_download_url
from services.analyze_tweets.spacy_matcher import filter_tweet, create_matcher_model, text_is_related_to_mental_health
from services.analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from services.analyze_tweets.translate_text import detect_and_translate_language
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from services.analyze_tweets.topic_modelling import load_model, apply_lda, tokenize_lemmatize_and_remove_stopwords, topic_modelling, NUM_TOPICS
from services.analyze_tweets.detect_coordinates import detect_coordinates
from services.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference
from services.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon

CURRENT_DIR = os.path.dirname(__file__)
TOPIC_MODEL_FILE = os.path.join(CURRENT_DIR, "services/topic_model/lda_model.model")
TOPIC_VALUES_FILE = os.path.join(CURRENT_DIR, "services/topic_model/topics.json")


def analyze_multiple_tweets(create_new_topic_model=False, time_period=5):

    # Download tweets from the Internet Archive Twitter Stream collection in the span of [period] minutes

    all_downloaded_tweets_list = []

    # Get the current time, but fix the year to 2022 because the Twitter Stream collection only contains tweets up to 2022
    starting_time = datetime.now().replace(year=2022, month=8)
    
    # Calculate the previous [period] minutes from the starting_time and download the tweets at that time
    for _ in range(time_period):
        starting_time -= timedelta(minutes=1)
        print(starting_time.strftime("%Y-%m-%d %H:%M:%S"))
        url = get_download_url(starting_time.year, starting_time.month, starting_time.day, starting_time.hour, starting_time.minute)
        # Download tweets
        downloaded_tweets = download_tweets(url)
        all_downloaded_tweets_list.extend(downloaded_tweets)

    # Analyze multiple tweet objects
    new_tweet_objects_list = []

    # ----------------------------------
    # Preprocess tweet text
    # ----------------------------------

    for tweet_object in all_downloaded_tweets_list:

        # Get the full, cleaned text of the tweet object
        # The 'text' key in the tweet object is not always the full text of the tweet, so we need to get the full text from the 'extended_tweet' key
        # We also need to clean the text to remove the URLs and handles and other noise
        tweet_text = clean_tweet_text(get_tweet_text(tweet_object))

        # Get the language of the tweet as detected by Twitter
        tweet_lang = tweet_object["lang"]

        # If the tweet is in English, skip the language detection and translation
        # Else, detect the language of the tweet and translate it to English
        if tweet_lang == "en":
            tweet_text_in_english = tweet_text
            tweet_lang_detected = "en"
        else:
            # continue
            # Detect the language of the tweet and translate it to English
            tweet_text_in_english, tweet_lang_detected, _, _ = detect_and_translate_language(tweet_text)

            if type(tweet_text_in_english) == list:
                print(tweet_text_in_english)
                tweet_text_in_english = tweet_text_in_english[0]

            if type(tweet_lang_detected) == list:
                print(tweet_lang_detected)
                tweet_lang_detected = tweet_lang_detected[0]

        # If the user's language is not detected, set it to the detected tweet language [1]
        if tweet_object['user']['lang'] == None:
            tweet_object['user']['lang'] = tweet_lang_detected

        # Text tokenized, lemmatized, and stemmed. You can change the tweet_text_in_english to just tweet_text if you want to keep the original language.
        tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(tweet_text_in_english)

        new_tweet_object = {
            **tweet_object,
            "text_analyzed": {
                "original": tweet_text,
                "in_english": tweet_text_in_english,
                "lang_detected": tweet_lang_detected,
                "processed": tweet_text_processed,
            }
        }

        new_tweet_objects_list.append(new_tweet_object)

    # ----------------------------------
    # Filter tweets
    # ----------------------------------

    # Filter all downloaded tweets to only contain mental health tweets 
    matcher_obj, nlp_obj = create_matcher_model()
    related_tweet_objects_list = [tweet_object for tweet_object in new_tweet_objects_list if text_is_related_to_mental_health(tweet_object['text_analyzed']['in_english'], matcher_obj, nlp_obj)]  # filter tweets to only contain mental health tweets
    
    tweets_amount_info = {
        "total": len(all_downloaded_tweets_list),
        "mentalhealthtweets": len(related_tweet_objects_list)
    }
    print(tweets_amount_info) # DEBUG

    new_tweet_objects_list = related_tweet_objects_list

    # ----------------------------------
    # Sentiment analysis of each tweet
    # ----------------------------------
    for tweet_object in new_tweet_objects_list:
        
        # We are using the English-translated text to feed to the sentiment analysis model
        text_to_analyze = tweet_object["text_analyzed"]["in_english"]

        sentiment_result, sentiment_confidence_probabilities = classify_sentiment(tweet_text_in_english)

        tweet_object["text_analyzed"]["sentiment"] = {
            "result": sentiment_result,
            "confidence_probabilities": sentiment_confidence_probabilities
        }

    # ----------------------------------
    # Topic modelling
    # ----------------------------------

    # We can choose to create a new topic model or load the existing one
    if create_new_topic_model:
        tweets_to_analyze = [tweet["text_analyzed"]["in_english"] for tweet in new_tweet_objects_list]
        lda_topic_model, topics_values = topic_modelling(tweets_to_analyze, num_topics=NUM_TOPICS)
    else:
        lda_topic_model = load_model(TOPIC_MODEL_FILE)
        topics_values = json.load(open(TOPIC_VALUES_FILE, "r"))

    # Get the keywords of the topic model
    keywords_of_topic_model = [[keyword for keyword, _ in topic] for topic in topics_values]

    # Topic modelling for each tweet
    for tweet_object in new_tweet_objects_list:
    
        text_to_analyze = tweet_object["text_analyzed"]["in_english"]
        
        topics_detected = apply_lda(text_to_analyze, lda_topic_model)
        
        # Convert float32 to float
        topics = [[topic[0], float(topic[1])] for topic in topics_detected]
        tweet_object["text_analyzed"]['topics'] = topics

        # Get the keywords associated with the tweet
        associated_keywords = [keyword for keyword in keywords_of_topic_model if keyword in text_to_analyze]
        tweet_object["text_analyzed"]['associated_keywords'] = associated_keywords

    return new_tweet_objects_list, tweets_amount_info, topics_values




def analyze_multiple_user(user_objects_list):
    '''
    Analyze multiple user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''

    new_user_object_list = []

    for user_object in user_objects_list:

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
            latitude, longitude = None, None
        else:
            latitude, longitude = coordinates[0], coordinates[1]

        # Detect polygon. This is to display the country name in the map.
        country_name = detect_geojson_ploygon(latitude, longitude)  # The country name key is "ADMIN" in the geojson file

        new_user_object_list.append(
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

    # Preprocess user object for m3inference
    users_demographics_input_list = []
    for user_object in new_user_object_list:
        user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, 
                                                                          id_key="id_str", 
                                                                          name_key="name",
                                                                          screen_name_key="screen_name",
                                                                          description_key="description",
                                                                          lang_key="lang",
                                                                          use_translator_if_necessary=True)

        users_demographics_input_list.append(user_object_preprocessed)

    # Detect demographics using m3inference
    users_demographics = detect_demographics(users_demographics_input_list)

    # For each user object, store the demographics detection result
    for user_object in new_user_object_list:
        user_object["demographics"] = users_demographics[user_object["id_str"]]

    return new_user_object_list



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
    lda_topic_model = load_model(TOPIC_MODEL_FILE)

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
    country_name = detect_geojson_ploygon(latitude, longitude)  # The country name key is "ADMIN" in the geojson file

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




