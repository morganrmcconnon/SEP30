from mongo_constants import DATABASE, CollectionNames

from services.download_tweets.download_tweets import download_tweets
from services.download_tweets.get_download_url import get_download_url

from services.analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from services.analyze_tweets.spacy_matcher import create_matcher_model, text_is_related_to_mental_health
from services.analyze_tweets.translate_text import detect_and_translate_language

from services.analyze_tweets.sentiment_analysis import classify_sentiment

from services.analyze_tweets.topic_modelling import apply_lda, tokenize_lemmatize_and_remove_stopwords, topic_modelling
from services.analyze_tweets.load_pretrained_topic_model import load_pretrained_model
from services.analyze_tweets.label_lda_topics import label_topics_from_preexisting_topic_model_and_keywords_list

from services.analyze_tweets.topic_cardiffnlp_tweet_topic import detect_topic_cardiffnlp_tweet_topic
from services.analyze_tweets.topic_bertopic_arxiv import detect_topics_bertopic_arxiv

from services.analyze_tweets.detect_coordinates import detect_coordinates
from services.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon 
from services.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference


SPACY_MATCHER_OBJ, SPACY_NLP_OBJ = create_matcher_model()


TOPICS_LABELS_MAP = label_topics_from_preexisting_topic_model_and_keywords_list()




def document_exists_in_collection(document_id, collection_name):
    return DATABASE[collection_name].count_documents({'_id': document_id}, limit = 1) >= 1


def load_document_value_from_collection(document_id, collection_name):
    return DATABASE[collection_name].find_one({'_id': document_id})['value']


def save_document_to_collection(document_to_insert, collection_name, id_key='_id'):
    collection = DATABASE[collection_name]
    if collection.count_documents({'_id': document_to_insert[id_key]}, limit = 1) == 0:
        collection.insert_one(document_to_insert)


def save_multiple_documents_to_collection(documents_to_insert, collection_name, id_key='_id'):
    collection = DATABASE[collection_name]
    documents_to_insert = [document for document in documents_to_insert if collection.count_documents({'_id': document[id_key]}, limit = 1) == 0]
    db_op_result = None
    if len(documents_to_insert) > 0:
        db_op_result = collection.insert_many(documents_to_insert)
    return db_op_result


def get_cached_value_or_perform_analysis(twitter_object, collection_name, analysis_function, id_key_name='id_str'):
    '''
    Get the cached value of the tweet object if it exists in the collection, else perform the analysis function and save the result to the collection

    The analysis function must take in a `tweet_object` and return a value that can be saved to the database

    The `id_key_name` is the key name of the tweet object that will be used as the document id in the collection
    '''
    twitter_obj_id = twitter_object[id_key_name]
    if document_exists_in_collection(twitter_obj_id, collection_name):
        analysis_value = load_document_value_from_collection(twitter_obj_id, collection_name)
    else:
        analysis_value = analysis_function(twitter_object)
        document_to_save = {
            '_id': twitter_obj_id,
            'value': analysis_value
        }
        save_document_to_collection(document_to_save, collection_name)
    
    twitter_object[collection_name] = analysis_value




def analysis_pipeline_analyze_multiple_tweets(tweet_objects: list, create_new_topic_model=False):
    
    tweet_count = len(tweet_objects) # DEBUG
    
    # ----------------------------------
    # Preprocess tweet text
    # ----------------------------------
    CollectionNames.tweet_text_original.value

    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_text_original.value, lambda tweet_object: clean_tweet_text(get_tweet_text(tweet_object)))        

    # ----------------------------------
    # Filter tweets before translating to English
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_filtered_pre_translation.value, lambda tweet_object: text_is_related_to_mental_health(tweet_object[CollectionNames.tweet_text_original.value], SPACY_MATCHER_OBJ, SPACY_NLP_OBJ))
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Filter pre {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    # ----------------------------------
    # Translate tweets to English
    # ----------------------------------
    def _translate(tweet_object):
        text = tweet_object[CollectionNames.tweet_text_original.value]
        translated_text, detected_language, _, _ = detect_and_translate_language(text)
        if type(translated_text) == list:
            translated_text = translated_text[0]
        if type(detected_language) == list:
            detected_language = detected_language[0]
        return {
            'in_english': translated_text,
            'lang_detected': detected_language
        }

    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_translated.value, lambda tweet_object: _translate(tweet_object))
        tweet_object['tweet_in_english'] = tweet_object[CollectionNames.tweet_translated.value]['in_english']
        tweet_object['tweet_lang_detected'] = tweet_object[CollectionNames.tweet_translated.value]['lang_detected']
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Translated {tweet_counter} / {tweet_count}')
        print('----------------------------------')

    
    # ----------------------------------
    # Filter tweets after translating to English
    # ----------------------------------
    # if filter_tweets and filter_after_translating:
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_filtered_post_translation.value, lambda tweet_object: text_is_related_to_mental_health(tweet_object['tweet_in_english'], SPACY_MATCHER_OBJ, SPACY_NLP_OBJ))
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Filter post {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    # ----------------------------------
    # Tokenize, lemmatize, and stem tweet text
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_processed.value, lambda tweet_object: tokenize_lemmatize_and_remove_stopwords(tweet_object['tweet_in_english']))
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Processed {tweet_counter} / {tweet_count}')
        print('----------------------------------')

    # ----------------------------------
    # Sentiment analysis of each tweet
    # ----------------------------------
    def _get_sentiment(tweet_object):
        tweet_text = tweet_object['tweet_in_english']
        sentiment, probabilities = classify_sentiment(tweet_text)
        return {
            'predicted': sentiment,
            'probabilities': probabilities
        }
    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_sentiment.value, lambda tweet_object: _get_sentiment(tweet_object))
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Sentiment {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    # ----------------------------------
    # Topic modelling using LDA
    # ----------------------------------
    # We can choose to create a new topic model or load the existing one
    if create_new_topic_model:
        texts_to_analyze = [tweet_object['tweet_in_english'] for tweet_object in tweet_objects]
        lda_topic_model, topics_values = topic_modelling(texts_to_analyze)
    else:
        lda_topic_model, topics_values = load_pretrained_model()

    # Get the keywords of the topic model
    keywords_of_topic_model = []
    for topic in topics_values.values():
        for keyword, _ in topic:
            if keyword not in keywords_of_topic_model:
                keywords_of_topic_model.append(keyword)

    def _get_topics_lda(tweet_object):
        topics_detected = apply_lda(tweet_object['tweet_in_english'], lda_topic_model)
        # Convert float32 to float
        topics_detected = [[topic[0], float(topic[1])] for topic in topics_detected]
        return topics_detected
    
    def _get_results_topics_lda(tweet_object):
        topics_detected = tweet_object[CollectionNames.tweet_topics_lda.value]
        text = tweet_object['tweet_in_english']
        highest_score_topic = max(topics_detected, key=lambda x: x[1])
        # Get the topic labels associated with the topic id
        topic_labels = TOPICS_LABELS_MAP.get(highest_score_topic[0], [])
        # Get the keywords associated with the tweet
        associated_keywords = [keyword for keyword in keywords_of_topic_model if keyword in text]
        return {
            'highest_score_topic': highest_score_topic[0],
            'highest_score_topic_probability': highest_score_topic[1],
            'topic_labels': topic_labels,
            'associated_keywords': associated_keywords
        }


    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG
    # Topic modelling for each tweet
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_topics_lda.value, lambda tweet_object: _get_topics_lda(tweet_object))

        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_topics_lda_results.value, lambda tweet_object: _get_results_topics_lda(tweet_object))

        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Topic {tweet_counter} / {tweet_count}')
        print('----------------------------------')

    # ----------------------------------
    # Topic modelling using BERTopic
    # ----------------------------------
    tweets_to_detect_topic = []
    for tweet_object in tweet_objects:
        tweet_id = tweet_object['id_str']
        if document_exists_in_collection(tweet_id, CollectionNames.tweet_topics_bertopic_arxiv.value):
            tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value] = load_document_value_from_collection(tweet_id, CollectionNames.tweet_topics_bertopic_arxiv.value)
        else:
            tweets_to_detect_topic.append(tweet_object)
    

    if len(tweets_to_detect_topic) > 0:
        texts_to_detect_topic = [tweet_object['tweet_in_english'] for tweet_object in tweets_to_detect_topic]
        topics_detected_list, topics_info_list, probs_detected_list = detect_topics_bertopic_arxiv(texts_to_detect_topic)
        documents_to_save = []
        for i in range(len(tweets_to_detect_topic)):
            topic_detected = int(topics_detected_list[i])
            topic_info = topics_info_list[i]
            probs_detected = float(probs_detected_list[i])
            tweet_object = tweets_to_detect_topic[i]
            tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value] = {
                'topic_id': topic_detected, 
                'probability': probs_detected,
                'topic_info': topic_info
            }
            document_to_save = {
                '_id': tweets_to_detect_topic[i]['id_str'],
                'value': tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value]
            }
            documents_to_save.append(document_to_save)
        db_op_result = save_multiple_documents_to_collection(documents_to_save, CollectionNames.tweet_topics_bertopic_arxiv.value)
        if db_op_result != None:
            print(f'Saved {len(db_op_result.inserted_ids)} tweet topics bertopic arxiv')
    
    # ----------------------------------
    # Topic inference using CardiffNLP Tweet Topic RoBERTa
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        get_cached_value_or_perform_analysis(tweet_object, CollectionNames.tweet_topics_cardiffnlp.value, lambda tweet_object: detect_topic_cardiffnlp_tweet_topic(tweet_object['tweet_in_english']))
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Tweet Topic CardiffNLP {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    return tweet_objects, topics_values


def analysis_pipeline_analyze_multiple_users(user_objects_list : list):
    '''
    Analyze multiple user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''
    user_count = len(user_objects_list) # DEBUG


    collection_name_user_location_translated = CollectionNames.user_location_translated.value
    collection_name_user_location_coordinates = CollectionNames.user_location_coordinates.value
    collection_name_user_location_country = CollectionNames.user_location_country.value


    def _translate_location(user_object):
        text = user_object['location']
        user_object['location_in_english'] = ''
        user_object['location_lang_detected'] = ''
        if text == None or text == '':
            return {
                'in_english': '',
                'lang_detected': ''
            }
        
        translated_text, detected_language, _, _ = detect_and_translate_language(text)
        
        if type(translated_text) == list:
            translated_text = translated_text[0]
        if type(detected_language) == list:
            detected_language = detected_language[0]

        if user_object['lang'] == None:
            user_object['lang'] = detected_language
        
        user_object['location_in_english'] = translated_text
        user_object['location_lang_detected'] = detected_language
        
        return {
            'in_english': translated_text,
            'lang_detected': detected_language
        }
    
    def _detect_coordinates(user_object):
        location_description = user_object['location']
        location_in_english = user_object[collection_name_user_location_translated]['in_english']
        location_lang = user_object[collection_name_user_location_translated]['lang_detected']
        if location_description == None or location_description == '':
            return {
                'latitude': None,
                'longitude': None,
            }
        try:
            coordinates = detect_coordinates(location_description, location_lang)
        except:
            coordinates = detect_coordinates(location_in_english)
        if coordinates == None:
            latitude = None
            longitude = None
        else:
            latitude = coordinates[0]
            longitude = coordinates[1]

        return {
            'latitude': latitude,
            'longitude': longitude,
        }

    def _detect_country(user_object):
        latitude = user_object[collection_name_user_location_coordinates]['latitude']
        longitude = user_object[collection_name_user_location_coordinates]['longitude']
        if latitude == None or longitude == None:
            return {
                'country_name': '',
                'country_code': ''
            }
        
        country_name = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key='name')
        country_code = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key='id')
        if country_name == None:
            country_name = ''
        if country_code == None:
            country_code = ''
        
        return {
            'country_name': country_name,
            'country_code': country_code
        }
    
    # ----------------------------------
    # Analyze the location of each user
    # ----------------------------------
    user_counter = 0 # DEBUG
    for user_object in user_objects_list:

        # Detect the language of the location description and translate it to English
        # Might be uneccessary if the user's lang is already defined

        get_cached_value_or_perform_analysis(user_object, collection_name_user_location_translated, lambda user_object: _translate_location(user_object))
        get_cached_value_or_perform_analysis(user_object, collection_name_user_location_coordinates, lambda user_object: _detect_coordinates(user_object))
        get_cached_value_or_perform_analysis(user_object, collection_name_user_location_country, lambda user_object: _detect_country(user_object))

        user_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Location {user_counter} / {user_count}')
        print('----------------------------------')


    # ----------------------------------
    # Detect demographics using m3inference
    # ----------------------------------
    collection_name_user_demographics = CollectionNames.user_demographics.value
    collection_name_user_m3_preprocessed = CollectionNames.user_m3_preprocessed.value

    user_objects_list_to_detect_demographics = []

    for user_object in user_objects_list:
        user_id = user_object['id_str']
        if document_exists_in_collection(user_id, collection_name_user_demographics) == False:
            user_objects_list_to_detect_demographics.append(user_object)
        else:
            user_object[collection_name_user_demographics] = load_document_value_from_collection(user_id, collection_name_user_demographics)
        
    # Preprocess user object for m3inference
    users_demographics_input_list = []
    user_counter = 0 # DEBUG
    user_count = len(user_objects_list_to_detect_demographics) # DEBUG
    for user_object in user_objects_list_to_detect_demographics:
        user_id = user_object['id_str']
        if document_exists_in_collection(user_id, collection_name_user_m3_preprocessed):
            user_object_preprocessed = load_document_value_from_collection(user_id, collection_name_user_m3_preprocessed)
        else:
            user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, 
                                                                          id_key='id_str', 
                                                                          name_key='name',
                                                                          screen_name_key='screen_name',
                                                                          description_key='description',
                                                                          lang_key='lang',
                                                                          use_translator_if_necessary=True)
            document_to_save = {
                '_id': user_id,
                'value': user_object_preprocessed
            }
            save_document_to_collection(document_to_save, collection_name_user_m3_preprocessed)

        users_demographics_input_list.append(user_object_preprocessed)

        user_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Preprocess M3 {user_counter} / {user_count}')
        print('----------------------------------')

    # Detect demographics using m3inference
    if len(users_demographics_input_list) > 0:
        users_demographics = detect_demographics(users_demographics_input_list)

    # For each user object, store the demographics detection result
    for user_object in user_objects_list_to_detect_demographics:
        user_object[collection_name_user_demographics] = users_demographics[user_object['id_str']]

    documents_to_save = [{
        '_id': user_id,
        'value': users_demographics[user_id]
    } for user_id in users_demographics.keys()]

    db_op_result = save_multiple_documents_to_collection(documents_to_save, collection_name_user_demographics)
    if db_op_result != None:
        print(f'Saved {len(db_op_result.inserted_ids)} user demographics')

    # ----------------------------------
    # Finalize the demographics prediction of each user
    # ----------------------------------
    def _user_demographics_result(user_object):
        user_demographics = user_object[collection_name_user_demographics]
        age_predicted = max(user_demographics['age'], key=user_demographics['age'].get)
        gender_predicted = max(user_demographics['gender'], key=user_demographics['gender'].get)
        org_predicted = max(user_demographics['org'], key=user_demographics['org'].get)
        return {
            'age_predicted': age_predicted,
            'gender_predicted': gender_predicted,
            'org_predicted': org_predicted
        }

    for user_object in user_objects_list:
        get_cached_value_or_perform_analysis(user_object, CollectionNames.user_demographics_result.value, lambda user_object: _user_demographics_result(user_object))

    return user_objects_list


def analysis_pipeline_download_tweets(url):
    # if url exist in collection urls, skip
    if DATABASE[CollectionNames.internet_archive_urls.value].count_documents({'url': url}, limit = 1) >= 1:
        print(f'URL {url} already exists in the database')
        downloaded_tweets_list = list(DATABASE['original_tweets'].find({'downloaded_from': url}))
    else:
        downloaded_tweets_list = download_tweets(url)
        print(f'Downloaded {len(downloaded_tweets_list)} tweets from {url}')
        for tweet_obj in downloaded_tweets_list:
            tweet_obj['downloaded_from'] = url
        # Save the url to the database
        DATABASE[CollectionNames.internet_archive_urls.value].insert_one({'url': url})

        # Insert all downloaded tweets into MongoDB collection. Set id_str as the primary key - `_id`
        # If the tweet with the same id_str already exists, do not insert it.
        documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in downloaded_tweets_list if DATABASE[CollectionNames.original_tweets.value].count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
        if len(documents_to_insert) > 0:
            db_op_result = DATABASE[CollectionNames.original_tweets.value].insert_many(documents_to_insert)
            print(f'Inserted {len(db_op_result.inserted_ids)} tweets')

    return downloaded_tweets_list


def analyze_data_by(year, month, day, hour, minute):

    url = get_download_url(year, month, day, hour, minute)
    print(url)

    downloaded_tweets_list = analysis_pipeline_download_tweets(url)
    
    # Analyze the tweet objects that are not cached
    analysis_pipeline_analyze_multiple_tweets(downloaded_tweets_list)

    # Analyze the users of the tweets
    user_objects_list = [tweet_object['user'] for tweet_object in downloaded_tweets_list]

    # Analyze the user objects that are not cached
    analysis_pipeline_analyze_multiple_users(user_objects_list)





