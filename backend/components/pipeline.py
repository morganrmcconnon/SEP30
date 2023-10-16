import os
from tqdm import tqdm

from constants import DATABASE, CollectionNames, DATA_LAKE_FOLDER, DataFolderNames

from components.download_tweets.download_tweets import download_tweets
from components.download_tweets.get_download_url import get_download_url

from components.analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from components.analyze_tweets.spacy_matcher import create_matcher_model, text_is_related_to_mental_health
from components.analyze_tweets.translate_text import detect_and_translate_language

from components.analyze_tweets.sentiment_analysis import classify_sentiment

from components.analyze_tweets.topic_modelling import apply_lda_model, tokenize_lemmatize_and_remove_stopwords, create_topic_model, get_keywords_of_topic_model
from components.analyze_tweets.topic_lda_labelling import get_similarity_scores, get_topics_distributions
from components.analyze_tweets.topic_lda_load_pretrained import load_pretrained_model

from components.analyze_tweets.topic_cardiffnlp_tweet_topic import detect_topic_cardiffnlp_tweet_topic
from components.analyze_tweets.topic_bertopic_arxiv import detect_topics_bertopic_arxiv, BERTOPIC_ARXIV_TOPIC_MODEL

from components.analyze_tweets.detect_coordinates import detect_coordinates
from components.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon 
from components.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference



SPACY_MATCHER_OBJ, SPACY_NLP_OBJ = create_matcher_model()

BERTOPIC_NAME_MAP = BERTOPIC_ARXIV_TOPIC_MODEL.get_topic_info().set_index('Topic')['Name'].to_dict()

def _save_topic_model_to_file_system(lda_topic_model, lda_topic_model_id):
    # Save the topic model binary to the file system
    model_directory = os.path.join(DATA_LAKE_FOLDER, DataFolderNames.lda_topic_models.value, lda_topic_model_id)
    print(model_directory)
    if os.path.exists(model_directory) == False:
        os.makedirs(model_directory, exist_ok=True)
        lda_topic_model.save(os.path.join(model_directory, "lda_topic_model.mdl"))
        print(f'Saved LDA topic model {lda_topic_model_id} to file system')


LDA_PRETRAINED_MODEL, LDA_TOPICS_REPRESENTATIONS = load_pretrained_model()

LDA_PRETRAINED_MODEL_ID = "0"


if DATABASE[CollectionNames.topic_models_lda.value].count_documents({"_id": LDA_PRETRAINED_MODEL_ID}, limit=1) == 0:
    LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS = get_topics_distributions(LDA_PRETRAINED_MODEL)
    db_op_result = DATABASE[CollectionNames.topic_models_lda.value].insert_one({
        "_id": LDA_PRETRAINED_MODEL_ID,
        "keywords_representation": LDA_TOPICS_REPRESENTATIONS,
        "labels": LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS
    })
    if db_op_result != None:
        print(f'Saved LDA topic model {LDA_PRETRAINED_MODEL_ID}')
else:
    LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS = DATABASE[CollectionNames.topic_models_lda.value].find_one({"_id": LDA_PRETRAINED_MODEL_ID}, limit=1)['labels']
    print(f'Loaded LDA topic model {LDA_PRETRAINED_MODEL_ID}')

_save_topic_model_to_file_system(LDA_PRETRAINED_MODEL, LDA_PRETRAINED_MODEL_ID)

KEYWORDS_OF_TOPIC_MODEL = get_keywords_of_topic_model(LDA_TOPICS_REPRESENTATIONS)



def _save_document_to_collection(document_to_insert, collection_name, id_key='_id'):
    collection = DATABASE[collection_name]
    if collection.count_documents({'_id': document_to_insert[id_key]}, limit = 1) == 0:
        collection.insert_one(document_to_insert)


def _save_multiple_documents_to_collection(documents_to_insert, collection_name, id_key='_id'):
    collection = DATABASE[collection_name]
    count_1 = len(documents_to_insert)
    documents_to_insert = [document for document in documents_to_insert if collection.count_documents({'_id': document[id_key]}, limit = 1) == 0]
    count_2 = len(documents_to_insert)
    print(f'Saving {count_2} / {count_1} documents')
    db_op_result = None
    if len(documents_to_insert) > 0:
        db_op_result = collection.insert_many(documents_to_insert)
    return db_op_result



def _get_cached_values_or_perform_analysis(twitter_object_list : list, collection_name : str, analysis_function, post_process_function = lambda tweet_object, analysis_value: None):
    '''
    Get the cached value of the tweet object if it exists in the collection, else perform the analysis function and save the result to the collection

    The analysis function must take in a `tweet_object` and return a value that can be saved to the database. It can optionally take in the list of tweet objects

    The post_process_function must take in a `tweet_object` and the analysis value and perform any post processing on the tweet object, regardless of whether the analysis value is cached or not. It can optionally take in the list of tweet objects

    In this function, the analysis value will be automatically saved to the tweet object as a new key that is equal to the name of the collection, and before the post_process_function is called
    '''
    ids_list = [twitter_object['id_str'] for twitter_object in twitter_object_list]
    documents_in_collection = DATABASE[collection_name].find({'_id': { '$in': ids_list }})
    documents_in_collection = {doc['_id']: doc['value'] for doc in documents_in_collection}
    with tqdm(total=len(twitter_object_list), desc=collection_name) as pbar:
        for twitter_object in twitter_object_list:
            twitter_obj_id = twitter_object['id_str']
            if twitter_obj_id in documents_in_collection:
                analysis_value = documents_in_collection[twitter_obj_id]
            else:
                analysis_value = analysis_function(twitter_object)
                document_to_save = {
                    '_id': twitter_obj_id,
                    'value': analysis_value
                }
                _save_document_to_collection(document_to_save, collection_name)
                # print('----------------------------------')
                # print(f'{collection_name} {obj_counter} / {obj_count}')
                # print('----------------------------------')    
            twitter_object[collection_name] = analysis_value
            post_process_function(twitter_object, analysis_value)
            pbar.update(1)

def _analysis_pipeline_preprocess_tweet_text(tweet_objects: list):
    # ----------------------------------
    # Preprocess tweet text
    # ----------------------------------
    _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_text_original.value, analysis_function=lambda tweet_object: clean_tweet_text(get_tweet_text(tweet_object)))


def _analysis_pipeline_feature_extract_tweet_objects(tweet_objects: list):
    # ----------------------------------
    # Feature extraction if necessary: Select only the necessary keys from the tweet object
    # ----------------------------------
    tweet_objects = [{
        'id_str': tweet_object['id_str'],
        'timestamp_ms': tweet_object['timestamp_ms'],
        'text': tweet_object['text'],
        'lang': tweet_object['lang'],
        'user': tweet_object['user'],
        CollectionNames.tweet_text_original.value: tweet_object[CollectionNames.tweet_text_original.value]
    } for tweet_object in tweet_objects]


def _analysis_pipeline_filter_tweets_spacy(tweet_objects: list, filter_after_translating=False):  

    if not filter_after_translating:
        # ----------------------------------
        # Filter tweets before translating to English
        # ----------------------------------
        _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_spacy_match_original.value, analysis_function=lambda tweet_object: text_is_related_to_mental_health(tweet_object[CollectionNames.tweet_text_original.value], SPACY_MATCHER_OBJ, SPACY_NLP_OBJ))    
    else:
        # ----------------------------------
        # Filter tweets after translating to English
        # ----------------------------------
        # if filter_tweets and filter_after_translating:
        _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_spacy_match_in_english.value, analysis_function=lambda tweet_object: text_is_related_to_mental_health(tweet_object[CollectionNames.tweet_translated.value]['in_english'], SPACY_MATCHER_OBJ, SPACY_NLP_OBJ))


def _analysis_pipeline_translate(tweet_objects: list):
    
    # ----------------------------------
    # Translate tweets to English
    # ----------------------------------
    def _translate(tweet_object):
        text = tweet_object[CollectionNames.tweet_text_original.value]
        lang = tweet_object['lang']
        if text == None or text == '':
            return {
                'in_english': '',
                'lang_detected': ''
            }
        if lang == 'en':
            return {
                'in_english': text,
                'lang_detected': 'en'
            }
        
        translated_text, detected_language, _, _ = detect_and_translate_language(text)
        if tweet_object["lang"] == None or tweet_object["lang"] == "und" or tweet_object["lang"] == "":
            tweet_object["lang"] = detected_language

        if type(translated_text) == list:
            translated_text = translated_text[0]
        if type(detected_language) == list:
            detected_language = detected_language[0]
        return {
            'in_english': translated_text,
            'lang_detected': detected_language
        }
    
    _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_translated.value, analysis_function=_translate)


def _analysis_pipeline_process_tweet_text(tweet_objects: list):
    # ----------------------------------
    # Tokenize, lemmatize, and stem tweet text
    # ----------------------------------
    _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_processed.value, analysis_function=lambda tweet_object: tokenize_lemmatize_and_remove_stopwords(tweet_object[CollectionNames.tweet_translated.value]['in_english']))



def _analysis_pipeline_sentiment(tweet_objects: list):
    # ----------------------------------
    # Sentiment analysis of each tweet
    # ----------------------------------
    def _get_sentiment(tweet_object):
        tweet_text = tweet_object[CollectionNames.tweet_translated.value]['in_english']
        sentiment, probabilities = classify_sentiment(tweet_text)
        return {
            'predicted': sentiment,
            'probabilities': probabilities
        }
    _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_sentiment.value, analysis_function=_get_sentiment)

def _analysis_pipeline_bertopic_arxiv(tweet_objects: list):
    # ----------------------------------
    # Topic inference using BERTopic Arxiv
    # ----------------------------------
    tweets_to_detect_topic = []
    tweet_ids = [tweet_object['id_str'] for tweet_object in tweet_objects]
    documents_in_collection = DATABASE[CollectionNames.tweet_topics_bertopic_arxiv.value].find({'_id': { '$in': tweet_ids }})
    documents_in_collection = {doc['_id']: doc['value'] for doc in documents_in_collection}
    for tweet_object in tweet_objects:
        tweet_id = tweet_object['id_str']
        if tweet_id in documents_in_collection:
            tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value] = documents_in_collection[tweet_id]
        else:
            tweets_to_detect_topic.append(tweet_object)
    

    if len(tweets_to_detect_topic) > 0:
        texts_to_detect_topic = [tweet_object[CollectionNames.tweet_translated.value]['in_english'] for tweet_object in tweets_to_detect_topic]
        topics_detected_list, probs_detected_list = detect_topics_bertopic_arxiv(texts_to_detect_topic)
        documents_to_save = []
        for i in range(len(tweets_to_detect_topic)):
            topic_detected = int(topics_detected_list[i])
            probs_detected = float(probs_detected_list[i])
            tweet_object = tweets_to_detect_topic[i]
            tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value] = {
                'topic_id': topic_detected, 
                'probability': probs_detected,
            }
            document_to_save = {
                '_id': tweets_to_detect_topic[i]['id_str'],
                'value': tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value]
            }
            documents_to_save.append(document_to_save)
        db_op_result = _save_multiple_documents_to_collection(documents_to_save, CollectionNames.tweet_topics_bertopic_arxiv.value)
        if db_op_result != None:
            print(f'Saved {len(db_op_result.inserted_ids)} tweet topics bertopic arxiv')


def _analysis_pipeline_tweet_topics_cardiffnlp(tweet_objects: list):
    # ----------------------------------
    # Topic inference using CardiffNLP Tweet Topic RoBERTa
    # ----------------------------------
    _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_topics_cardiffnlp.value, analysis_function=lambda tweet_object: detect_topic_cardiffnlp_tweet_topic(tweet_object[CollectionNames.tweet_translated.value]['in_english']))

def _analysis_pipeline_lda_topic_modelling(tweet_objects: list, create_new_topic_model=False):
    # ----------------------------------
    # Topic modelling using LDA
    # ----------------------------------
    # We can choose to create a new topic model or load the existing one
    if create_new_topic_model:
        texts_to_analyze = [tweet_object[CollectionNames.tweet_translated.value]['in_english'] for tweet_object in tweet_objects]
        lda_topic_model, lda_topics_representations = create_topic_model(texts_to_analyze)
        lda_labels_topics_distributions = get_topics_distributions(lda_topic_model)
        keywords_of_topic_model = get_keywords_of_topic_model(lda_topics_representations)
        
        db_op_result = DATABASE[CollectionNames.topic_models_lda.value].insert_one({
            "keywords_representation": lda_topics_representations,
            "labels": lda_labels_topics_distributions
        })
        if db_op_result != None:
            # Advice: Change the way the topic model id is generated
            lda_topic_model_id = db_op_result.inserted_id
            print(f'Saved LDA topic model {lda_topic_model_id}')

        _save_topic_model_to_file_system(lda_topic_model, lda_topic_model_id)
        
    else:
        # Convert keys to string for MongoDB
        lda_topic_model = LDA_PRETRAINED_MODEL
        lda_topics_representations = LDA_TOPICS_REPRESENTATIONS
        lda_topic_model_id = LDA_PRETRAINED_MODEL_ID
        lda_labels_topics_distributions = LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS
        keywords_of_topic_model = KEYWORDS_OF_TOPIC_MODEL
        

    def _get_topics_lda(tweet_object):
        text = tweet_object[CollectionNames.tweet_translated.value]['in_english']
        topics_distribution = apply_lda_model(text, lda_topic_model)
        highest_score_topic = max(topics_distribution, key=lambda x: x[1])
        # Calculate the similarity scores of the topic labels to the tweet
        related_topics_cossim = get_similarity_scores(lda_labels_topics_distributions, topics_distribution, method="cossim")
        related_topics_cossim.sort(key=lambda x: x[1], reverse=True)
        related_topics_hellinger = get_similarity_scores(lda_labels_topics_distributions, topics_distribution, method="hellinger")
        related_topics_hellinger.sort(key=lambda x: x[1], reverse=False)
        # Get the keywords associated with the tweet
        associated_keywords = [[keywords_of_topic ,[keyword for keyword in keywords_of_topic if keyword in text]] for keywords_of_topic in keywords_of_topic_model.values()]
        return {
            'model_id': lda_topic_model_id,
            'topics_distribution': topics_distribution,
            'highest_score_topic': highest_score_topic[0],
            'highest_score_topic_probability': highest_score_topic[1],
            'related_topics': {
                'cosine_similarity': related_topics_cossim,
                'hellinger_distance': related_topics_hellinger, 
            },
            'associated_keywords': associated_keywords
        }
    
    _get_cached_values_or_perform_analysis(tweet_objects, CollectionNames.tweet_topics_lda.value, analysis_function=_get_topics_lda)


    return tweet_objects, lda_topics_representations


def _analysis_pipeline_analyze_multiple_tweets(tweet_objects: list, create_new_topic_model=False):
    '''
    Analyze multiple user object
    
    The keys in the object follows the Twitter API v1.1 dictionary.
    '''

    _analysis_pipeline_preprocess_tweet_text(tweet_objects)
    _analysis_pipeline_feature_extract_tweet_objects(tweet_objects)
    _analysis_pipeline_filter_tweets_spacy(tweet_objects, filter_after_translating=False)
    _analysis_pipeline_translate(tweet_objects)
    _analysis_pipeline_filter_tweets_spacy(tweet_objects, filter_after_translating=True)
    _analysis_pipeline_process_tweet_text(tweet_objects)
    _analysis_pipeline_sentiment(tweet_objects)
    _analysis_pipeline_bertopic_arxiv(tweet_objects)
    _analysis_pipeline_tweet_topics_cardiffnlp(tweet_objects)
    tweet_objects, lda_topics_values = _analysis_pipeline_lda_topic_modelling(tweet_objects, create_new_topic_model=create_new_topic_model)

    return tweet_objects, lda_topics_values


def _analysis_pipeline_feature_extract_user_objects(user_objects_list : list):

    # ----------------------------------
    # Feature extraction if necessary: Select only the necessary keys from the object
    # ----------------------------------
    user_objects_list = [{
        'id_str': user_object['id_str'],
        'name': user_object['name'],
        'screen_name': user_object['screen_name'],
        'description': user_object['description'],
        'lang': user_object['lang'],
        'location': user_object['location']
    } for user_object in user_objects_list]

def _analysis_pipeline_location_analysis(user_objects_list : list):    
    # ----------------------------------
    # Analyze the location of each user
    # ----------------------------------

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
        
        return {
            'in_english': translated_text,
            'lang_detected': detected_language
        }
    
    def _post_process_translate_location(user_object, analysis_value):
        user_object['location_in_english'] = analysis_value['in_english']
        user_object['location_lang_detected'] = analysis_value['lang_detected']
        
        if user_object['lang'] == None:
            user_object['lang'] = analysis_value['lang_detected']

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
    
    # def _post_process_detect_coordinates(user_object, analysis_value):
    #     user_object['location_latitude'] = analysis_value['latitude']
    #     user_object['location_longitude'] = analysis_value['longitude']

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
    
    # def _post_process_detect_country(user_object, analysis_value):
    #     user_object['location_country_name'] = analysis_value['country_name']
    #     user_object['location_country_code'] = analysis_value['country_code']
    
    _get_cached_values_or_perform_analysis(user_objects_list, collection_name_user_location_translated, analysis_function=_translate_location, post_process_function=_post_process_translate_location)
    _get_cached_values_or_perform_analysis(user_objects_list, collection_name_user_location_coordinates, analysis_function=_detect_coordinates)
    _get_cached_values_or_perform_analysis(user_objects_list, collection_name_user_location_country, analysis_function=_detect_country)


def _analysis_pipeline_demographics_analysis(user_objects_list : list):
    # ----------------------------------
    # Detect demographics using m3inference
    # ----------------------------------
    collection_name_user_demographics = CollectionNames.user_demographics.value
    collection_name_user_m3_preprocessed = CollectionNames.user_m3_preprocessed.value


    # Check if the user demographics is already cached

    ids_list = [user_object['id_str'] for user_object in user_objects_list]

    documents_containing_ids = DATABASE[collection_name_user_demographics].find({'_id': { '$in': ids_list }})
    
    documents_dict = {doc['_id']: doc['value'] for doc in documents_containing_ids}
    
    user_objects_list_to_detect_demographics = []
    for user_object in user_objects_list:
        user_id = user_object['id_str']
        if user_id in documents_dict:
            user_object[collection_name_user_demographics] = documents_dict[user_id]
        else:
            user_objects_list_to_detect_demographics.append(user_object)


    # Check if the user m3 preprocessed format is already cached
    documents_containing_ids = DATABASE[collection_name_user_m3_preprocessed].find({'_id': { '$in': ids_list }})
    
    documents_dict = {doc['_id']: doc['value'] for doc in documents_containing_ids}

    # Preprocess user object for m3inference
    users_demographics_input_list = []

    with tqdm(total=len(user_objects_list_to_detect_demographics), desc=collection_name_user_m3_preprocessed) as pbar:    
        for user_object in user_objects_list_to_detect_demographics:
            user_id = user_object['id_str']
            if user_id in documents_dict:
                user_object_preprocessed = documents_dict[user_id]
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
                _save_document_to_collection(document_to_save, collection_name_user_m3_preprocessed)


            users_demographics_input_list.append(user_object_preprocessed)
            pbar.update(1)


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

        db_op_result = _save_multiple_documents_to_collection(documents_to_save, collection_name_user_demographics)
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

    _get_cached_values_or_perform_analysis(user_objects_list, CollectionNames.user_demographics_result.value, analysis_function=_user_demographics_result)




def _analysis_pipeline_analyze_multiple_users(user_objects_list : list):
    '''
    Analyze multiple user object
    
    The keys in the object follows the Twitter API v1.1 dictionary.
    '''
    _analysis_pipeline_feature_extract_user_objects(user_objects_list)
    _analysis_pipeline_location_analysis(user_objects_list)
    _analysis_pipeline_demographics_analysis(user_objects_list)
    return user_objects_list


def _analysis_pipeline_combine_feature_extract_and_save(analyzed_tweets : list, analyzed_users : list):
    # ----------------------------------
    # Combine the analyzed tweets and users and save to the database
    # ----------------------------------

    # Feature extraction if necessary: Select only the necessary keys from the object
    
    # Feature extract users first
    users_map = {}
    for user_object in analyzed_users:
        user_id = user_object['id_str']
        new_user_object = {
            'id_str': user_id,
            "country_code": user_object[CollectionNames.user_location_country.value]["country_code"],
            "country_name": user_object[CollectionNames.user_location_country.value]["country_name"],
            "age": user_object[CollectionNames.user_demographics_result.value]["age_predicted"],
            "gender": user_object[CollectionNames.user_demographics_result.value]["gender_predicted"],
            "org": user_object[CollectionNames.user_demographics_result.value]["org_predicted"],
            "lang": user_object["lang"],
        }
        # for collection_name in CollectionNames:
        #     if collection_name.value in user_object:
        #         new_user_object[collection_name.value] = user_object[collection_name.value]
        users_map[user_id] = new_user_object

    # Feature extract tweets. Add the user object to the tweet object.
    # This will be used to save the analyzed tweets to the database
    documents_to_save = []
    with tqdm(total=len(analyzed_tweets), desc=CollectionNames.analyzed_tweets.value) as pbar:
        for tweet_object in analyzed_tweets:
            user_id = tweet_object['user']['id_str']
            user_object = users_map[user_id]
            
            related_topics_cosine_similarity = tweet_object[CollectionNames.tweet_topics_lda.value]["related_topics"]["cosine_similarity"]
            cosine_similarity_benchmark = 0.5
            related_topics_cosine_similarity = [related_topics_cosine_similarity[0][0]] + [topic[0] for topic in related_topics_cosine_similarity[1:5] if topic[1] > cosine_similarity_benchmark]
            
            related_topics_hellinger_distance = tweet_object[CollectionNames.tweet_topics_lda.value]["related_topics"]["hellinger_distance"]
            hellinger_distance_benchmark = 0.5
            related_topics_hellinger_distance = [related_topics_hellinger_distance[0][0]] + [topic[0] for topic in related_topics_hellinger_distance[1:5] if topic[1] < hellinger_distance_benchmark]

            topic_bert_arxiv_id = tweet_object[CollectionNames.tweet_topics_bertopic_arxiv.value]["topic_id"]
            topic_bert_arxiv_name = BERTOPIC_NAME_MAP[topic_bert_arxiv_id]
            
            document_to_save = {
                '_id': tweet_object['id_str'],
                'id_str': tweet_object['id_str'],
                'timestamp_ms': tweet_object['timestamp_ms'],
                "text": tweet_object[CollectionNames.tweet_text_original.value],
                "text_in_english": tweet_object[CollectionNames.tweet_translated.value]["in_english"],
                "text_processed": tweet_object[CollectionNames.tweet_processed.value],
                "lang": tweet_object["lang"],
                "spacy_match": {
                    "original": tweet_object[CollectionNames.tweet_spacy_match_original.value],
                    "in_english": tweet_object[CollectionNames.tweet_spacy_match_in_english.value],
                },
                "sentiment": tweet_object[CollectionNames.tweet_sentiment.value]["predicted"],
                "topic_lda": {
                    'model_id': tweet_object[CollectionNames.tweet_topics_lda.value]["model_id"],
                    'topic_id': tweet_object[CollectionNames.tweet_topics_lda.value]["highest_score_topic"],                    'related_topics': {
                        'cosine_similarity': related_topics_cosine_similarity,
                        'hellinger_distance': related_topics_hellinger_distance,
                    },
                },
                "topic_bert_arxiv": {
                    "topic_id": topic_bert_arxiv_id,
                    "topic_name": topic_bert_arxiv_name,
                },
                "topic_cardiffnlp": max(tweet_object[CollectionNames.tweet_topics_cardiffnlp.value], key=lambda x: x["topic_score"]),
                "user": user_object,
            }
            # for collection_name in CollectionNames:
            #     if collection_name.value in tweet_object:
            #         document_to_save[collection_name.value] = tweet_object[collection_name.value]
            # # Add the user object to the tweet object
            # user_id = tweet_object['user']['id_str']
            # document_to_save['user'] = users_map[user_id]
            documents_to_save.append(document_to_save)
            pbar.update(1)

    # Insert or update the analyzed tweets to the database
    db_op_result = _save_multiple_documents_to_collection(documents_to_save, CollectionNames.analyzed_tweets.value, id_key='_id')
    if db_op_result != None:
        print(f'Inserted {len(db_op_result.inserted_ids)} tweets')


    return documents_to_save


def analysis_pipeline_full(tweets_list, create_new_topic_model=False):

    # Analyze the tweet objects
    analyzed_tweets, lda_topic_values = _analysis_pipeline_analyze_multiple_tweets(tweets_list, create_new_topic_model=create_new_topic_model)

    # Analyze the users of the tweets
    user_objects_list = [tweet_object['user'] for tweet_object in analyzed_tweets]

    # Analyze the user objects that are not cached
    analyzed_users = _analysis_pipeline_analyze_multiple_users(user_objects_list)


    # Combine the analyzed tweets and users and save to the database
    # Also feature extraction if necessary. Select only the necessary keys from the object
    _analysis_pipeline_combine_feature_extract_and_save(analyzed_tweets, analyzed_users)


def analysis_pipeline_download_tweets(url):
    # if url exist in collection urls, skip
    if DATABASE[CollectionNames.internet_archive_urls.value].count_documents({'_id': url}, limit = 1) >= 1:
        print(f'URL {url} already exists in the database')
        downloaded_tweets_list = list(DATABASE[CollectionNames.original_tweets.value].find({'downloaded_from': url}))
    else:
        downloaded_tweets_list = download_tweets(url)
        print(f'Downloaded {len(downloaded_tweets_list)} tweets from {url}')
        for tweet_obj in downloaded_tweets_list:
            tweet_obj['downloaded_from'] = url
        # Save the url to the database

        # Insert all downloaded tweets into MongoDB collection. Set id_str as the primary key - `_id`
        # If the tweet with the same id_str already exists, do not insert it.
        documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in downloaded_tweets_list]

        db_op_result = _save_multiple_documents_to_collection(documents_to_insert, CollectionNames.original_tweets.value, id_key='_id')
        if db_op_result != None:
            print(f'Inserted {len(db_op_result.inserted_ids)} tweets')

        # We need to confirm that all tweets are saved into the database before we save the url to the database.
        DATABASE[CollectionNames.internet_archive_urls.value].insert_one({'_id': url})

    return downloaded_tweets_list 



def analyze_data_by(year, month, day, hour, minute):

    url = get_download_url(year, month, day, hour, minute)
    print(url)

    downloaded_tweets_list = analysis_pipeline_download_tweets(url)

    analysis_pipeline_full(downloaded_tweets_list, create_new_topic_model=False) 
    