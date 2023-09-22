from datetime import datetime, timedelta
import os
import json
import pymongo

if __name__ == '__main__':

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
    TOPIC_MODEL_FILE = os.path.join(CURRENT_DIR, 'services/topic_model/lda_model.model')
    TOPIC_VALUES_FILE = os.path.join(CURRENT_DIR, 'services/topic_model/topics.json')



    COLLECTIONS_LIST = [ 
        'original_tweets', 
        'analyzed_tweets', 
        'analyzed_users', 
        'internet_archive_urls',
        'tweet_translated',
        'tweet_filtered_pre_translation',
        'tweet_filtered_post_translation',
        'tweet_processed',
        'tweet_sentiment',
        'tweet_topics',
        'user_location_translated',
        'user_location_coordinates',
        'user_m3_preprocessed',
        'user_demographics'
    ]

    # Establish connection with MongoDB
    MONGODB_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')

    # Get database and collection

    # create a new database if it doesn't exist
    if 'twitter_db' not in MONGODB_CLIENT.list_database_names():
        DATABASE = MONGODB_CLIENT['twitter_db']
    else:
        DATABASE = MONGODB_CLIENT['twitter_db']

    # create new collections if it doesn't exist
    for collection_name in COLLECTIONS_LIST:
        if collection_name not in DATABASE.list_collection_names():
            DATABASE.create_collection(collection_name)
        else:
            print(f'Collection {collection_name} already exists')    


def object_exists_in_collection(object_id, collection_name):
    return DATABASE[collection_name].count_documents({'_id': object_id}, limit = 1) >= 1

def load_object_from_collection(object_id, collection_name):
    return DATABASE[collection_name].find_one({'_id': object_id})


def save_document_to_collection(document_to_insert, collection_name, id_key='_id'):
    collection = DATABASE[collection_name]
    if collection.count_documents({'_id': document_to_insert[id_key]}, limit = 1) == 0:
        collection.insert_one(document_to_insert)


def analyze_multiple_tweets(tweet_objects: list, create_new_topic_model=False, filter_tweets=False, filter_after_translating=True):
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
        tweet_object['text_analyzed'] = {
            'original': tweet_text,
            'is_mental_health_related': True,
            'is_mental_health_related_pre_translation': False,
            'is_mental_health_related_post_translation': False,
            'in_english': '',
            'lang_detected': '',
            'processed': [],
            'sentiment': {
                'negative': 0,
                'positive': 0,
                'neutral': 0
            },
            'sentiment_predicted': '',
            'topics': [],
            'topic_with_the_highest_score': '',
            'associated_keywords': []
        }

    # ----------------------------------
    # Filter tweets before translating to English
    # ----------------------------------

    matcher_obj, nlp_obj = create_matcher_model()
    
    for tweet_object in tweet_objects:
        if object_exists_in_collection(tweet_object['id_str'], 'tweet_filtered_pre_translation'):
            saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_filtered_pre_translation')
            tweet_object['text_analyzed']['is_mental_health_related_pre_translation'] = saved_object['is_mental_health_related_pre_translation']
        else:
            tweet_object['text_analyzed']['is_mental_health_related_pre_translation'] = text_is_related_to_mental_health(tweet_object['text_analyzed']['original'], matcher_obj, nlp_obj)
            object_to_save = {
                '_id': tweet_object['id_str'],
                'is_mental_health_related_pre_translation': tweet_object['text_analyzed']['is_mental_health_related_pre_translation']
            }
            save_document_to_collection(object_to_save, 'tweet_filtered_pre_translation')


    # ----------------------------------
    # Translate tweets to English
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG

    for tweet_object in tweet_objects:

        tweet_id = tweet_object['id_str']

        tweet_text = tweet_object['text_analyzed']['original']

        # Get the language of the tweet as detected by Twitter
        tweet_lang = tweet_object['lang']
        print(tweet_lang)


        if object_exists_in_collection(tweet_id, 'tweet_translated'):
            saved_object = load_object_from_collection(tweet_id, 'tweet_translated')
            tweet_text_in_english = saved_object['in_english']
            tweet_lang_detected = saved_object['lang_detected']

        else:    
            # If the tweet is in English, skip the language detection and translation
            # Else, detect the language of the tweet and translate it to English
            if tweet_lang == 'en':
                tweet_text_in_english = tweet_text
                tweet_lang_detected = 'en'
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
            object_to_save = {
                '_id': tweet_id,
                'in_english': tweet_text_in_english,
                'lang_detected': tweet_lang_detected
            }
            save_document_to_collection(object_to_save, 'tweet_translated')

        
        print(tweet_text_in_english)
        print(tweet_lang_detected)

        # If the user's language is not detected, set it to the detected tweet language [1]
        if tweet_object['user']['lang'] == None:
            tweet_object['user']['lang'] = tweet_lang_detected

        
        tweet_object['text_analyzed']['in_english'] = tweet_text_in_english
        tweet_object['text_analyzed']['lang_detected'] = tweet_lang_detected

        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'{tweet_counter} / {tweet_count}')
        print('----------------------------------')

    
    # ----------------------------------
    # Filter tweets after translating to English
    # ----------------------------------
    # if filter_tweets and filter_after_translating:

    for tweet_object in tweet_objects:
        if object_exists_in_collection(tweet_object['id_str'], 'tweet_filtered_post_translation'):
            saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_filtered_post_translation')
            tweet_object['text_analyzed']['is_mental_health_related_post_translation'] = saved_object['is_mental_health_related_post_translation']
        else:
            tweet_object['text_analyzed']['is_mental_health_related_post_translation'] = text_is_related_to_mental_health(tweet_object['text_analyzed']['in_english'], matcher_obj, nlp_obj)
            object_to_save = {
                '_id': tweet_object['id_str'],
                'is_mental_health_related_post_translation': tweet_object['text_analyzed']['is_mental_health_related_post_translation']
            }
            save_document_to_collection(object_to_save, 'tweet_filtered_post_translation')



    # ----------------------------------
    # Sentiment analysis of each tweet
    # ----------------------------------
    for tweet_object in tweet_objects:
        
        # We are using the English-translated text to feed to the sentiment analysis model
        text_to_analyze = tweet_object['text_analyzed']['in_english']

        
        # Text tokenized, lemmatized, and stemmed. You can change the tweet_text_in_english to just tweet_text if you want to keep the original language.
        if object_exists_in_collection(tweet_object['id_str'], 'tweet_processed'):
            saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_processed')
            tweet_text_processed = saved_object['processed']
        else:    
            tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(text_to_analyze)
            tweet_object['text_analyzed']['processed'] = tweet_text_processed
            object_to_save = {
                '_id': tweet_object['id_str'],
                'processed': tweet_text_processed
            }
            save_document_to_collection(object_to_save, 'tweet_processed')

        # Sentiment analysis
        if object_exists_in_collection(tweet_object['id_str'], 'tweet_sentiment'):
            saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_sentiment')
            sentiment_predicted = saved_object['sentiment_predicted']
            sentiment_confidence_probabilities = saved_object['sentiment']
        else:
            sentiment_predicted, sentiment_confidence_probabilities = classify_sentiment(text_to_analyze)
            tweet_object['text_analyzed']['sentiment'] = sentiment_confidence_probabilities
            tweet_object['text_analyzed']['sentiment_predicted'] = sentiment_predicted
            object_to_save = {
                '_id': tweet_object['id_str'],
                'sentiment_predicted': sentiment_predicted,
                'sentiment': sentiment_confidence_probabilities
            }
            save_document_to_collection(object_to_save, 'tweet_sentiment')

    # ----------------------------------
    # Topic modelling
    # ----------------------------------

    # We can choose to create a new topic model or load the existing one
    if create_new_topic_model:
        tweets_to_analyze = [tweet_object['text_analyzed']['in_english'] for tweet_object in tweet_objects if tweet_object['text_analyzed']['is_mental_health_related']]
        lda_topic_model, topics_values = topic_modelling(tweets_to_analyze, num_topics=NUM_TOPICS)
    else:
        lda_topic_model = load_model(TOPIC_MODEL_FILE)
        topics_values = json.load(open(TOPIC_VALUES_FILE, 'r'))

    # Get the keywords of the topic model
    keywords_of_topic_model = []
    for topic in topics_values.values():
        for keyword, _ in topic:
            if keyword not in keywords_of_topic_model:
                keywords_of_topic_model.append(keyword)

    # Topic modelling for each tweet
    for tweet_object in tweet_objects:
    
        text_to_analyze = tweet_object['text_analyzed']['in_english']

        if object_exists_in_collection(tweet_object['id_str'], 'tweet_topics'):
            saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_topics')
            topics = saved_object['topics']
        else:
            topics_detected = apply_lda(text_to_analyze, lda_topic_model)
            # Convert float32 to float
            topics = [[topic[0], float(topic[1])] for topic in topics_detected]
            object_to_save = {
                '_id': tweet_object['id_str'],
                'topics': topics
            }
            save_document_to_collection(object_to_save, 'tweet_topics')

        tweet_object['text_analyzed']['topics'] = topics
        
        tweet_object['text_analyzed']['topic_with_the_highest_score'] = max(topics, key=lambda x: x[1])[0]

        # Get the keywords associated with the tweet
        associated_keywords = [keyword for keyword in keywords_of_topic_model if keyword in text_to_analyze]
        tweet_object['text_analyzed']['associated_keywords'] = associated_keywords

    return tweet_objects, topics_values


def analyze_multiple_users(user_objects_list : list):
    '''
    Analyze multiple user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''
    # Initialize the location_analyzed and demographics keys in the user object
    for user_object in user_objects_list:
        user_object['location_analyzed'] = {
            'in_english': '',
            'lang_detected': '',
            'latitude': None,
            'longitude': None,
            'country_name': '',
            'country_code': ''
        }
        user_object['demographics'] = {
            'age': {
                '19-29': 0,
                '30-39': 0,
                '<=18': 0,
                '>=40': 0
            },
            'gender': {
                'female': 0, 
                'male': 0
            },
            'org': {
                'is-org': 0, 
                'non-org': 0
            }
        }
        user_object['age_predicted'] = ''
        user_object['gender_predicted'] = ''
        user_object['org_predicted'] = ''

    # Analyze the location of each user
    user_counter = 0 # DEBUG
    user_count = len(user_objects_list) # DEBUG
    for user_object in user_objects_list:

        # Get original location description
        location_description = user_object['location']

        if(location_description == None or location_description == ''):
            continue

        # Detect the language of the location description and translate it to English
        # Might be uneccessary if the user's lang is already defined
        if object_exists_in_collection(user_object['id_str'], 'user_location_translated'):
            saved_object = load_object_from_collection(user_object['id_str'], 'user_location_translated')
            location_in_english = saved_object['in_english']
            location_lang_detected = saved_object['lang_detected']
        else:
            location_in_english, location_lang_detected, _, _ = detect_and_translate_language(location_description)
            object_to_save = {
                '_id': user_object['id_str'],
                'in_english': location_in_english,
                'lang_detected': location_lang_detected
            }
            save_document_to_collection(object_to_save, 'user_location_translated')

        # If the language is not detected, set it to the detected location language, or the tweet's language (See [1] in this code file)
        if user_object['lang'] == None:
            user_object['lang'] = location_lang_detected

        # Detect coordinates
        if object_exists_in_collection(user_object['id_str'], 'user_location_coordinates'):
            saved_object = load_object_from_collection(user_object['id_str'], 'user_location_coordinates')
            latitude = saved_object['latitude']
            longitude = saved_object['longitude']
            country_name = saved_object['country_name']
            country_code = saved_object['country_code']

        else:            
            coordinates = detect_coordinates(location_description, language=location_lang_detected)

            if coordinates == None:
                latitude = None
                longitude = None
                country_name = ''
                country_code = ''

            else:
                latitude = coordinates[0]
                longitude = coordinates[1]

                # Detect polygon. This is to display the country name in the map.
                country_name = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key='name')
                country_code = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key='id')
                if country_name == None:
                    country_name = ''
            
            object_to_save = {
                '_id': user_object['id_str'],
                'latitude': latitude,
                'longitude': longitude,
                'country_name': country_name,
                'country_code': country_code
            }
            save_document_to_collection(object_to_save, 'user_location_coordinates')


        user_object['location_analyzed'] = {
            'in_english': location_in_english,
            'lang_detected': location_lang_detected,
            'latitude': latitude,
            'longitude': longitude,
            'country_name': country_name,
            'country_code': country_code
        }

        user_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'{user_counter} / {user_count}')
        print('----------------------------------')

    user_objects_list_to_detect_demographics = []

    for user_object in user_objects_list:
        if object_exists_in_collection(user_object['id_str'], 'user_demographics') == False:
            user_objects_list_to_detect_demographics.append(user_object)
        else:
            user_object['demographics'] = load_object_from_collection(user_object['id_str'], 'user_demographics')['demographics']
        
    # Preprocess user object for m3inference
    users_demographics_input_list = []
    user_counter = 0 # DEBUG
    user_count = len(user_objects_list_to_detect_demographics) # DEBUG
    for user_object in user_objects_list_to_detect_demographics:
        if object_exists_in_collection(user_object['id_str'], 'user_m3_preprocessed'):
            saved_object = load_object_from_collection(user_object['id_str'], 'user_m3_preprocessed')
            user_object_preprocessed = saved_object['user_object_preprocessed']
        else:
            user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, 
                                                                          id_key='id_str', 
                                                                          name_key='name',
                                                                          screen_name_key='screen_name',
                                                                          description_key='description',
                                                                          lang_key='lang',
                                                                          use_translator_if_necessary=True)
            object_to_save = {
                '_id': user_object['id_str'],
                'user_object_preprocessed': user_object_preprocessed
            }
            save_document_to_collection(object_to_save, 'user_m3_preprocessed')

        users_demographics_input_list.append(user_object_preprocessed)

        user_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'{user_counter} / {user_count}')
        print('----------------------------------')

    # Detect demographics using m3inference
    if len(users_demographics_input_list) > 0:
        users_demographics = detect_demographics(users_demographics_input_list)

    # For each user object, store the demographics detection result
    for user_object in user_objects_list_to_detect_demographics:
        user_object['demographics'] = users_demographics[user_object['id_str']]

    documents_to_save = [{
        '_id': user_id,
        'demographics': users_demographics[user_id]
    } for user_id in users_demographics.keys()]

    # Remove duplicate user id
    

    if len(documents_to_save) > 0:
        db_op_result = DATABASE['user_demographics'].insert_many(documents_to_save)
        print(f'Saved {len(db_op_result.inserted_ids)} user demographics')

    for user_object in user_objects_list:
        user_object['age_predicted'] = max(user_object['demographics']['age'], key=user_object['demographics']['age'].get)
        user_object['gender_predicted'] = max(user_object['demographics']['gender'], key=user_object['demographics']['gender'].get)
        user_object['org_predicted'] = max(user_object['demographics']['org'], key=user_object['demographics']['org'].get)


    return user_objects_list



def analyze_data_by(year, month, day, hour, minute):

    url = get_download_url(year, month, day, hour, minute)
    print(url)

    # if url exist in colelction urls, skip
    url_exists = DATABASE['internet_archive_urls'].count_documents({'url': url}, limit = 1) >= 1

    if url_exists:
        print(f'URL {url} already exists in the database')
        all_downloaded_tweets_list = list(DATABASE['original_tweets'].find({'downloaded_from': url}))
    else:
        all_downloaded_tweets_list = download_tweets(url)
        for tweet_obj in all_downloaded_tweets_list:
            tweet_obj['downloaded_from'] = url
        # Save the url to the database
        DATABASE['internet_archive_urls'].insert_one({'url': url})

    # Insert all downloaded tweets into MongoDB collection. Set id_str as the primary key - `_id`
    # If the tweet with the same id_str already exists, do not insert it.
    documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in all_downloaded_tweets_list if DATABASE['original_tweets'].count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
    if len(documents_to_insert) > 0:
        db_op_result = DATABASE['original_tweets'].insert_many(documents_to_insert)
        print(f'Inserted {len(db_op_result.inserted_ids)} tweets')

    # If a tweet with the same id_str already exists, do not analyze it.
    list_of_tweets_to_analyze = [tweet_object for tweet_object in all_downloaded_tweets_list if DATABASE['analyzed_tweets'].count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
    
    # Analyze the tweet objects that are not cached
    analyzed_tweets, topics_values = analyze_multiple_tweets(list_of_tweets_to_analyze)

    # Save analyzed tweets into MongoDB collection. Set id_str as the primary key - `_id`
    # If the tweet with the same id_str already exists, do not insert it.
    documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in analyzed_tweets if DATABASE['analyzed_tweets'].count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
    if len(documents_to_insert) > 0:
        db_op_result = DATABASE['analyzed_tweets'].insert_many(documents_to_insert)
        print(f'Saved {len(db_op_result.inserted_ids)} analyzed tweets')


    # Analyze the users of the tweets
    user_objects_list = [tweet_object['user'] for tweet_object in all_downloaded_tweets_list]

    # If a user with the same id_str already exists, do not analyze it.
    list_of_users_to_analyze = [user_object for user_object in user_objects_list if DATABASE['analyzed_users'].count_documents({'_id': user_object['id_str']}, limit = 1) == 0]

    # Analyze the user objects that are not cached
    analyzed_users = analyze_multiple_users(list_of_users_to_analyze)

    # Save analyzed users into MongoDB collection. Set id_str as the primary key - `_id`
    # If the user with the same id_str already exists, do not insert it.
    documents_to_insert = [{**user_object, '_id': user_object['id_str']} for user_object in analyzed_users if DATABASE['analyzed_users'].count_documents({'_id': user_object['id_str']}, limit = 1) == 0]
    # Remove documents with duplicate ids
    documents_to_insert = {document['_id']: document for document in documents_to_insert}.values()
    if len(documents_to_insert) > 0:
        db_op_result = DATABASE['analyzed_users'].insert_many(documents_to_insert)
        print(f'Saved {len(db_op_result.inserted_ids)} analyzed users')

if __name__ == '__main__':    
    # Get the current time, but fix the year to 2022 because the Twitter Stream collection only contains tweets up to 2022
    starting_time = datetime(2022, 8, 31, 23, 59, 0)
    # Calculate the previous [period] minutes from the starting_time and download the tweets at that time
    time_period = 10100
    for _ in range(time_period):
        analyze_data_by(starting_time.year, starting_time.month, starting_time.day, starting_time.hour, starting_time.minute)
        starting_time -= timedelta(minutes=1)

