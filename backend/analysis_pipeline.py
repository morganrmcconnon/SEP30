from datetime import datetime, timedelta

from services.download_tweets.download_tweets import download_tweets
from services.download_tweets.get_download_url import get_download_url
from services.analyze_tweets.spacy_matcher import create_matcher_model, text_is_related_to_mental_health
from services.analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from services.analyze_tweets.translate_text import detect_and_translate_language
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from services.analyze_tweets.topic_modelling import apply_lda, tokenize_lemmatize_and_remove_stopwords, topic_modelling, NUM_TOPICS
from services.analyze_tweets.load_pretrained_topic_model import load_pretrained_model
from services.analyze_tweets.detect_coordinates import detect_coordinates
from services.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference
from services.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon


def download_tweets_during_time_period(time_period=1):

    # Download tweets from the Internet Archive Twitter Stream collection in the span of [period] minutes

    all_downloaded_tweets_list = []

    # Get the current time, but fix the year to 2022 because the Twitter Stream collection only contains tweets up to 2022
    starting_time = datetime.now().replace(year=2022, month=9, day=1, hour=0, minute=0)
    
    # Calculate the previous [period] minutes from the starting_time and download the tweets at that time
    for _ in range(time_period):
        starting_time -= timedelta(minutes=1)
        print(starting_time.strftime("%Y-%m-%d %H:%M:%S"))
        url = get_download_url(starting_time.year, starting_time.month, starting_time.day, starting_time.hour, starting_time.minute)
        # Download tweets
        print(starting_time)
        print(url)
        downloaded_tweets = download_tweets(url)
        print(starting_time)
        print(url)
        all_downloaded_tweets_list.extend(downloaded_tweets)

    # Analyze multiple tweet objects

    print(len(all_downloaded_tweets_list))

    return all_downloaded_tweets_list


def analyze_multiple_tweets(tweet_objects: list, create_new_topic_model=False, filter_tweets=True, filter_after_translating=True):
    # ----------------------------------
    # Preprocess tweet text
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG

    for tweet_object in tweet_objects:

        # Get the full, cleaned text of the tweet object
        # The 'text' key in the tweet object is not always the full text of the tweet, so we need to get the full text from the 'extended_tweet' key
        # We also need to clean the text to remove the URLs and handles and other noise
        tweet_text = clean_tweet_text(get_tweet_text(tweet_object))
        print(tweet_text)
        tweet_object["text_analyzed"] = {
            "original": tweet_text,
            "is_mental_health_related": True,
            "in_english": "",
            "lang_detected": "",
            "processed": [],
            "sentiment": {
                "negative": 0,
                "positive": 0,
                "neutral": 0
            },
            "sentiment_predicted": "",
            "topics": [],
            "topic_with_the_highest_score": "",
            "associated_keywords": []
        }

    # ----------------------------------
    # Filter tweets before translating to English
    # ----------------------------------

    if filter_tweets and not filter_after_translating:

        # Filter all tweets to only contain mental health tweets 
        matcher_obj, nlp_obj = create_matcher_model()

        for tweet_object in tweet_objects:
            tweet_object["text_analyzed"]["is_mental_health_related"] = text_is_related_to_mental_health(tweet_object["text_analyzed"]["original"], matcher_obj, nlp_obj)


    # ----------------------------------
    # Translate tweets to English
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG

    for tweet_object in tweet_objects:

        if not tweet_object["text_analyzed"]["is_mental_health_related"]:
            continue

        tweet_text = tweet_object["text_analyzed"]["original"]

        # Get the language of the tweet as detected by Twitter
        tweet_lang = tweet_object["lang"]
        print(tweet_lang)

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
        print(tweet_text_in_english)
        print(tweet_lang_detected)

        # If the user's language is not detected, set it to the detected tweet language [1]
        if tweet_object['user']['lang'] == None:
            tweet_object['user']['lang'] = tweet_lang_detected

        
        tweet_object["text_analyzed"]["in_english"] = tweet_text_in_english
        tweet_object["text_analyzed"]["lang_detected"] = tweet_lang_detected

        tweet_counter += 1 # DEBUG
        print("----------------------------------")
        print(f"{tweet_counter} / {tweet_count}")
        print("----------------------------------")

    
    # ----------------------------------
    # Filter tweets after translating to English
    # ----------------------------------
    if filter_tweets and filter_after_translating:

        # Filter all tweets to only contain mental health tweets 
        matcher_obj, nlp_obj = create_matcher_model()

        for tweet_object in tweet_objects:
            tweet_object["text_analyzed"]["is_mental_health_related"] = text_is_related_to_mental_health(tweet_object["text_analyzed"]["in_english"], matcher_obj, nlp_obj)



    # ----------------------------------
    # Sentiment analysis of each tweet
    # ----------------------------------
    for tweet_object in tweet_objects:

        if not tweet_object["text_analyzed"]["is_mental_health_related"]:
            continue
        
        # We are using the English-translated text to feed to the sentiment analysis model
        text_to_analyze = tweet_object["text_analyzed"]["in_english"]

        
        # Text tokenized, lemmatized, and stemmed. You can change the tweet_text_in_english to just tweet_text if you want to keep the original language.
        tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(text_to_analyze)
        tweet_object["text_analyzed"]["processed"] = tweet_text_processed

        sentiment_predicted, sentiment_confidence_probabilities = classify_sentiment(text_to_analyze)
        tweet_object["text_analyzed"]["sentiment"] = sentiment_confidence_probabilities
        tweet_object["text_analyzed"]["sentiment_predicted"] = sentiment_predicted

    # ----------------------------------
    # Topic modelling
    # ----------------------------------

    # We can choose to create a new topic model or load the existing one
    if create_new_topic_model:
        tweets_to_analyze = [tweet_object["text_analyzed"]["in_english"] for tweet_object in tweet_objects if tweet_object["text_analyzed"]["is_mental_health_related"]]
        lda_topic_model, topics_values = topic_modelling(tweets_to_analyze, num_topics=NUM_TOPICS)
    else:
        lda_topic_model, topics_values = load_pretrained_model()

    # Get the keywords of the topic model
    keywords_of_topic_model = []
    for topic in topics_values.values():
        for keyword, _ in topic:
            if keyword not in keywords_of_topic_model:
                keywords_of_topic_model.append(keyword)

    # Topic modelling for each tweet
    for tweet_object in tweet_objects:
        if not tweet_object["text_analyzed"]["is_mental_health_related"]:
            continue
    
        text_to_analyze = tweet_object["text_analyzed"]["in_english"]
        
        topics_detected = apply_lda(text_to_analyze, lda_topic_model)
        
        # Convert float32 to float
        topics = [[topic[0], float(topic[1])] for topic in topics_detected]
        tweet_object["text_analyzed"]['topics'] = topics
        tweet_object["text_analyzed"]['topic_with_the_highest_score'] = max(topics, key=lambda x: x[1])[0]

        # Get the keywords associated with the tweet
        associated_keywords = [keyword for keyword in keywords_of_topic_model if keyword in text_to_analyze]
        tweet_object["text_analyzed"]['associated_keywords'] = associated_keywords

    return tweet_objects, topics_values


def analyze_multiple_users(user_objects_list):
    '''
    Analyze multiple user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''
    # Initialize the location_analyzed and demographics keys in the user object
    for user_object in user_objects_list:
        user_object["location_analyzed"] = {
            "in_english": "",
            "lang_detected": "",
            "latitude": None,
            "longitude": None,
            "country_name": "",
            "country_code": ""
        }
        user_object["demographics"] = {
            'age': {
                '19-29': 0.1546,
                '30-39': 0.114,
                '<=18': 0.0481,
                '>=40': 0.6833
            },
            'gender': {
                'female': 0.0066, 
                'male': 0.9934
            },
            'org': {
                'is-org': 0.7508, 
                'non-org': 0.2492
            }
        }
        user_object["age_predicted"] = ""
        user_object["gender_predicted"] = ""
        user_object["org_predicted"] = ""

    # Analyze the location of each user
    for user_object in user_objects_list:

        # Get original location description
        location_description = user_object["location"]

        if(location_description == None or location_description == ""):
            continue

        # Detect the language of the location description and translate it to English
        # Might be uneccessary if the user's lang is already defined
        location_in_english, location_lang_detected, _, _ = detect_and_translate_language(location_description)

        # If the language is not detected, set it to the detected location language, or the tweet's language (See [1] in this code file)
        if user_object['lang'] == None:
            user_object['lang'] = location_lang_detected

        # Detect coordinates
        coordinates = detect_coordinates(location_description, language=location_lang_detected)

        if coordinates == None:
            latitude = None
            longitude = None
            country_name = ""
            country_code = ""

        else:
            latitude = coordinates[0]
            longitude = coordinates[1]

            # Detect polygon. This is to display the country name in the map.
            country_name = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key="name")  # The country name key is "ADMIN" in the geojson file
            country_code = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key="id")  # The country code key is "ISO_A3" in the geojson file

        user_object["location_analyzed"] = {
            "in_english": location_in_english,
            "lang_detected": location_lang_detected,
            "latitude": latitude,
            "longitude": longitude,
            "country_name": country_name,
            "country_code": country_code
        }
        
    # Preprocess user object for m3inference
    users_demographics_input_list = []
    for user_object in user_objects_list:
        user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, 
                                                                          id_key="id_str", 
                                                                          name_key="name",
                                                                          screen_name_key="screen_name",
                                                                          description_key="description",
                                                                          lang_key="lang",
                                                                          use_translator_if_necessary=True)

        users_demographics_input_list.append(user_object_preprocessed)

    # Detect demographics using m3inference
    if len(users_demographics_input_list) > 0:
        users_demographics = detect_demographics(users_demographics_input_list)

    # For each user object, store the demographics detection result
    for user_object in user_objects_list:
        user_object["demographics"] = users_demographics[user_object["id_str"]]
        user_object["age_predicted"] = max(user_object["demographics"]["age"], key=user_object["demographics"]["age"].get)
        user_object["gender_predicted"] = max(user_object["demographics"]["gender"], key=user_object["demographics"]["gender"].get)
        user_object["org_predicted"] = max(user_object["demographics"]["org"], key=user_object["demographics"]["org"].get)


    return user_objects_list


def aggregate_tweet_objects_analysis_result(tweet_objects_list):
    
    sentiment_count = {"negative": 0, "positive": 0, "neutral": 0}

    topics_count = {i : 0 for i in range(NUM_TOPICS)}

    keywords_count = {}

    keywords_pairs = {}

    for tweet_object in tweet_objects_list:
        # print(tweet_object)
        text_analyzed_result = tweet_object["text_analyzed"]

        # ---------topic processing----------#
        highest_score_topic = text_analyzed_result["topic_with_the_highest_score"]
        topics_count[highest_score_topic] = topics_count.get(highest_score_topic, 0) + 1
        # ---------topic processing----------#

        # ---------sentiment processing----------#
        sentiment_predicted = text_analyzed_result["sentiment_predicted"]
        sentiment_count[sentiment_predicted] = sentiment_count.get(sentiment_predicted, 0) + 1
        # ---------sentiment processing----------#


        keywords = text_analyzed_result["associated_keywords"]

        # ---------keyword count----------#
        for keyword in keywords:
            keywords_count[keyword] = keywords_count.get(keyword, 0) + 1

        # ---------keyword pairs----------#
        # For each pair of keywords, add the pair to the dictionary and increment the count
        if len(keywords) > 1:
            for i in range(len(keywords)):
                for j in range(i+1, len(keywords)):
                    keywords_pair = (keywords[i], keywords[j]) if keywords[i] < keywords[j] else (keywords[j], keywords[i])
                    keywords_pairs[keywords_pair] = keywords_pairs.get(keywords_pair, 0) + 1

    keywords_pairs = [{"keywords": list(keywords_pair), "count": count} for keywords_pair, count in keywords_pairs.items()]

    return topics_count, sentiment_count, keywords_count, keywords_pairs


def aggregate_user_objects_analysis_result(data):
    countries_count = {}

    genders_count = { "female": 0, "male": 0 }

    age_groups_count = { "<=18": 0, "19-29": 0, "30-39": 0, ">=40": 0 }

    org_count = { "is-org": 0, "non-org": 0 }

    for user_object in data:
        # print(user_object)

        # ---------location processing----------#
        country_code = user_object["location_analyzed"]["country_code"]
        countries_count[country_code] = countries_count.get(country_code, 0) + 1
        # ---------location processing----------#

        # ---------gender processing----------#
        gender = user_object["gender_predicted"]
        genders_count[gender] += 1

        # ---------age processing----------#
        age = user_object["age_predicted"]
        age_groups_count[age] += 1

        org = user_object["org_predicted"]
        org_count[org] += 1

    return countries_count, genders_count, age_groups_count, org_count

