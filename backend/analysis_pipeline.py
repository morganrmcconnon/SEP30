import pymongo

from services.download_tweets.download_tweets import download_tweets
from services.download_tweets.get_download_url import get_download_url
from services.analyze_tweets.spacy_matcher import create_matcher_model, text_is_related_to_mental_health
from services.analyze_tweets.tweet_text import get_tweet_text, clean_tweet_text
from services.analyze_tweets.translate_text import detect_and_translate_language
from services.analyze_tweets.sentiment_analysis import classify_sentiment
from services.analyze_tweets.topic_modelling import apply_lda, tokenize_lemmatize_and_remove_stopwords, topic_modelling, NUM_TOPICS
from services.analyze_tweets.load_pretrained_topic_model import load_pretrained_model
from services.analyze_tweets.label_lda_topics import label_topics_from_preexisting_topic_model_and_keywords_list
from services.analyze_tweets.detect_coordinates import detect_coordinates
from services.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference
from services.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon
from services.analyze_tweets.topic_cardiffnlp_tweet_topic import detect_topic_cardiffnlp_tweet_topic
from services.analyze_tweets.topic_bertopic_arxiv import detect_topics_bertopic_arxiv


SPACY_MATCHER_OBJ, SPACY_NLP_OBJ = create_matcher_model()

TOPICS_LABELS = label_topics_from_preexisting_topic_model_and_keywords_list()


COLLECTIONS_LIST = [ 
    'original_tweets',
    'internet_archive_urls',
    'tweet_translated',
    'tweet_filtered_pre_translation',
    'tweet_filtered_post_translation',
    'tweet_processed',
    'tweet_sentiment',
    'tweet_topics_lda',
    'tweet_topics_lda_results',
    'tweet_topics_bertopic_arxiv',
    'tweet_topics_cardiffnlp',
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


def document_exists_in_collection(document_id, collection_name):
    return DATABASE[collection_name].count_documents({'_id': document_id}, limit = 1) >= 1


def load_object_from_collection(object_id, collection_name):
    return DATABASE[collection_name].find_one({'_id': object_id})


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


def analyze_tweet_preprocess_tweet_text(tweet_object):
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
        'topic_bertopic_arxiv': [],
        'topic_with_the_highest_score': '',
        'associated_keywords': []
    }

    return tweet_object


def analyze_tweet_filter_tweet_pre_translation(tweet_object):
    if document_exists_in_collection(tweet_object['id_str'], 'tweet_filtered_pre_translation'):
        saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_filtered_pre_translation')
        tweet_object['text_analyzed']['is_mental_health_related_pre_translation'] = saved_object['is_mental_health_related_pre_translation']
    else:
        tweet_object['text_analyzed']['is_mental_health_related_pre_translation'] = text_is_related_to_mental_health(tweet_object['text_analyzed']['original'], SPACY_MATCHER_OBJ, SPACY_NLP_OBJ)
        document_to_save = {
            '_id': tweet_object['id_str'],
            'is_mental_health_related_pre_translation': tweet_object['text_analyzed']['is_mental_health_related_pre_translation']
        }
        save_document_to_collection(document_to_save, 'tweet_filtered_pre_translation')

    return tweet_object


def analyze_tweet_translate_tweet(tweet_object):
    tweet_id = tweet_object['id_str']

    tweet_text = tweet_object['text_analyzed']['original']

    # Get the language of the tweet as detected by Twitter
    tweet_lang = tweet_object['lang']
    print(tweet_lang)


    if document_exists_in_collection(tweet_id, 'tweet_translated'):
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
        document_to_save = {
            '_id': tweet_id,
            'in_english': tweet_text_in_english,
            'lang_detected': tweet_lang_detected
        }
        save_document_to_collection(document_to_save, 'tweet_translated')

    
    print(tweet_text_in_english)
    print(tweet_lang_detected)

    # If the user's language is not detected, set it to the detected tweet language [1]
    if tweet_object['user']['lang'] == None:
        tweet_object['user']['lang'] = tweet_lang_detected

    
    tweet_object['text_analyzed']['in_english'] = tweet_text_in_english
    tweet_object['text_analyzed']['lang_detected'] = tweet_lang_detected

    return tweet_object


def analyze_tweet_filter_tweet_post_translation(tweet_object):
    if document_exists_in_collection(tweet_object['id_str'], 'tweet_filtered_post_translation'):
        saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_filtered_post_translation')
        tweet_object['text_analyzed']['is_mental_health_related_post_translation'] = saved_object['is_mental_health_related_post_translation']
    else:
        tweet_object['text_analyzed']['is_mental_health_related_post_translation'] = text_is_related_to_mental_health(tweet_object['text_analyzed']['in_english'], SPACY_MATCHER_OBJ, SPACY_NLP_OBJ)
        document_to_save = {
            '_id': tweet_object['id_str'],
            'is_mental_health_related_post_translation': tweet_object['text_analyzed']['is_mental_health_related_post_translation']
        }
        save_document_to_collection(document_to_save, 'tweet_filtered_post_translation')

    return tweet_object


def analyze_tweet_tokenize_lemmatize_and_remove_stopwords(tweet_object):
    text_to_analyze = tweet_object['text_analyzed']['in_english']

    # Text tokenized, lemmatized, and stemmed. You can change the tweet_text_in_english to just tweet_text if you want to keep the original language.
    if document_exists_in_collection(tweet_object['id_str'], 'tweet_processed'):
        saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_processed')
        tweet_text_processed = saved_object['processed']
    else:    
        tweet_text_processed = tokenize_lemmatize_and_remove_stopwords(text_to_analyze)
        document_to_save = {
            '_id': tweet_object['id_str'],
            'processed': tweet_text_processed
        }
        save_document_to_collection(document_to_save, 'tweet_processed')

    tweet_object['text_analyzed']['processed'] = tweet_text_processed

    return tweet_object


def analyze_tweet_sentiment(tweet_object):
    # We are using the English-translated text to feed to the sentiment analysis model
    text_to_analyze = tweet_object['text_analyzed']['in_english']

    # Sentiment analysis
    if document_exists_in_collection(tweet_object['id_str'], 'tweet_sentiment'):
        saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_sentiment')
        sentiment_predicted = saved_object['sentiment_predicted']
        sentiment_confidence_probabilities = saved_object['sentiment']
    else:
        sentiment_predicted, sentiment_confidence_probabilities = classify_sentiment(text_to_analyze)
        document_to_save = {
            '_id': tweet_object['id_str'],
            'sentiment_predicted': sentiment_predicted,
            'sentiment': sentiment_confidence_probabilities
        }
        save_document_to_collection(document_to_save, 'tweet_sentiment')

    tweet_object['text_analyzed']['sentiment'] = sentiment_confidence_probabilities
    tweet_object['text_analyzed']['sentiment_predicted'] = sentiment_predicted

    return tweet_object


def analyze_multiple_tweets_topic_modelling_lda(tweet_objects: list, create_new_topic_model=False):
    # We can choose to create a new topic model or load the existing one
    if create_new_topic_model:
        tweets_to_analyze = [tweet_object['text_analyzed']['in_english'] for tweet_object in tweet_objects if tweet_object['text_analyzed']['is_mental_health_related']]
        lda_topic_model, topics_values = topic_modelling(tweets_to_analyze, num_topics=NUM_TOPICS)
    else:
        lda_topic_model, topics_values = load_pretrained_model()

    # Get the keywords of the topic model
    keywords_of_topic_model = []
    for topic in topics_values.values():
        for keyword, _ in topic:
            if keyword not in keywords_of_topic_model:
                keywords_of_topic_model.append(keyword)

    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG
    # Topic modelling for each tweet
    for tweet_object in tweet_objects:
    
        text_to_analyze = tweet_object['text_analyzed']['in_english']

        if document_exists_in_collection(tweet_object['id_str'], 'tweet_topics'):
            saved_object = load_object_from_collection(tweet_object['id_str'], 'tweet_topics')
            topics = saved_object['topics']
        else:
            topics_detected = apply_lda(text_to_analyze, lda_topic_model)
            # Convert float32 to float
            topics = [[topic[0], float(topic[1])] for topic in topics_detected]
            document_to_save = {
                '_id': tweet_object['id_str'],
                'topics': topics,
            }
            save_document_to_collection(document_to_save, 'tweet_topics')

        tweet_object['text_analyzed']['topics'] = topics

        # Get the topic with the highest score
        highest_score_topic = max(topics, key=lambda x: x[1])
        tweet_object['text_analyzed']['highest_score_topic'] = highest_score_topic[0]
        tweet_object['text_analyzed']['highest_score_topic_probability'] = highest_score_topic[1]
        # Get the topic labels associated with the topic id
        topic_labels = TOPICS_LABELS.get(highest_score_topic[0], {})
        tweet_object['text_analyzed']['topic_labels'] = topic_labels
        # Get the keywords associated with the tweet
        associated_keywords = [keyword for keyword in keywords_of_topic_model if keyword in text_to_analyze]
        tweet_object['text_analyzed']['associated_keywords'] = associated_keywords

        if document_exists_in_collection(tweet_object['id_str'], 'tweet_topics_lda_results') == False:
            document_to_save = {
                '_id': tweet_object['id_str'],
                'highest_score_topic': highest_score_topic[0],
                'highest_score_topic_probability': highest_score_topic[1],
                'topic_labels': topic_labels,
                'associated_keywords': associated_keywords
            }
            save_document_to_collection(document_to_save, 'tweet_topics_lda_results')

        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Topic {tweet_counter} / {tweet_count}')
        print('----------------------------------')

    return tweet_objects, topics_values


def analyze_multiple_tweets_topic_modelling_bertopic_arxiv(tweet_objects: list):
    tweets_to_detect_topic = []
    for tweet_object in tweet_objects:
        if document_exists_in_collection(tweet_object['id_str'], 'tweet_topics_bertopic_arxiv'):
            tweet_object['text_analyzed']['topic_bertopic_arxiv'] = load_object_from_collection(tweet_object['id_str'], 'tweet_topics_bertopic_arxiv')['result']
        else:
            tweets_to_detect_topic.append(tweet_object)
    

    if len(tweets_to_detect_topic) > 0:
        texts_to_detect_topic = [tweet_object['text_analyzed']['in_english'] for tweet_object in tweets_to_detect_topic]
        topics_detected_list, topics_info_list, probs_detected_list = detect_topics_bertopic_arxiv(texts_to_detect_topic)
        documents_to_save = []
        for i in range(len(tweets_to_detect_topic)):
            topic_detected = int(topics_detected_list[i])
            topic_info = topics_info_list[i]
            probs_detected = float(probs_detected_list[i])
            tweet_object = tweets_to_detect_topic[i]
            tweet_object['text_analyzed']['topic_bertopic_arxiv'] = {
                'topic_id': topic_detected, 
                'probability': probs_detected,
                'topic_info': topic_info
            }
            document_to_save = {
                '_id': tweets_to_detect_topic[i]['id_str'],
                'result': tweet_object['text_analyzed']['topic_bertopic_arxiv']
            }
            documents_to_save.append(document_to_save)
        db_op_result = save_multiple_documents_to_collection(documents_to_save, 'tweet_topics_bertopic_arxiv')
        if db_op_result != None:
            print(f'Saved {len(db_op_result.inserted_ids)} tweet topics bertopic arxiv')

    return tweet_objects


def analyze_multiple_tweets_topic_modelling_cardiffnlp_tweet_topic(tweet_object):
    # We are using the English-translated text to feed to the model
    text_to_analyze = tweet_object['text_analyzed']['in_english']
    tweet_id = tweet_object['id_str']

    if document_exists_in_collection(tweet_object['id_str'], 'tweet_topics_cardiffnlp'):
        saved_object = load_object_from_collection(tweet_id, 'tweet_topics_cardiffnlp')
        topics = saved_object['topics']
    else:
        topics = detect_topic_cardiffnlp_tweet_topic(text_to_analyze)
        document_to_save = {
            '_id': tweet_id,
            'topics': topics
        }
        save_document_to_collection(document_to_save, 'tweet_sentiment')

    tweet_object['text_analyzed']['tweet_topics_cardiffnlp'] = topics

    return tweet_object


def analyze_multiple_tweets(tweet_objects: list, create_new_topic_model=False, filter_tweets=False, filter_after_translating=True):
    
    tweet_count = len(tweet_objects) # DEBUG
    
    # ----------------------------------
    # Preprocess tweet text
    # ----------------------------------
    for tweet_object in tweet_objects:
        analyze_tweet_preprocess_tweet_text(tweet_object)
        

    # ----------------------------------
    # Filter tweets before translating to English
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        analyze_tweet_filter_tweet_pre_translation(tweet_object)
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Filter pre {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    # ----------------------------------
    # Translate tweets to English
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        analyze_tweet_translate_tweet(tweet_object)
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
        analyze_tweet_filter_tweet_post_translation(tweet_object)
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Filter post {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    # ----------------------------------
    # Tokenize, lemmatize, and stem tweet text
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        analyze_tweet_tokenize_lemmatize_and_remove_stopwords(tweet_object)
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Processed {tweet_counter} / {tweet_count}')
        print('----------------------------------')

    # ----------------------------------
    # Sentiment analysis of each tweet
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    tweet_count = len(tweet_objects) # DEBUG
    for tweet_object in tweet_objects:
        analyze_tweet_sentiment(tweet_object)
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Sentiment {tweet_counter} / {tweet_count}')
        print('----------------------------------')

    # ----------------------------------
    # Topic modelling using LDA
    # ----------------------------------
    tweet_objects, topics_values = analyze_multiple_tweets_topic_modelling_lda(tweet_objects, create_new_topic_model=create_new_topic_model)
    
    # ----------------------------------
    # Topic modelling using BERTopic
    # ----------------------------------
    analyze_multiple_tweets_topic_modelling_bertopic_arxiv(tweet_objects)
    
    # ----------------------------------
    # Topic inference using CardiffNLP Tweet Topic RoBERTa
    # ----------------------------------
    tweet_counter = 0 # DEBUG
    for tweet_object in tweet_objects:
        analyze_multiple_tweets_topic_modelling_cardiffnlp_tweet_topic(tweet_object)
        tweet_counter += 1 # DEBUG
        print('----------------------------------')
        print(f'Tweet Topic CardiffNLP {tweet_counter} / {tweet_count}')
        print('----------------------------------')


    return tweet_objects, topics_values

def analyze_multiple_users(user_objects_list : list):
    '''
    Analyze multiple user object
    
    The keys in the user object follows the Twitter API v1.1 dictionary.
    '''
    user_count = len(user_objects_list) # DEBUG

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
            'age': { '19-29': 0, '30-39': 0, '<=18': 0, '>=40': 0 },
            'gender': { 'female': 0,  'male': 0 },
            'org': { 'is-org': 0,  'non-org': 0 }
        }
        user_object['age_predicted'] = ''
        user_object['gender_predicted'] = ''
        user_object['org_predicted'] = ''

        return user_object

    # ----------------------------------
    # Analyze the location of each user
    # ----------------------------------
    user_counter = 0 # DEBUG
    for user_object in user_objects_list:

        # Get original location description
        location_description = user_object['location']

        if(location_description == None or location_description == ''):
            continue

        # Detect the language of the location description and translate it to English
        # Might be uneccessary if the user's lang is already defined
        if document_exists_in_collection(user_object['id_str'], 'user_location_translated'):
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
        if document_exists_in_collection(user_object['id_str'], 'user_location_coordinates'):
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


    # ----------------------------------
    # Detect demographics using m3inference
    # ----------------------------------
    user_objects_list_to_detect_demographics = []

    for user_object in user_objects_list:
        if document_exists_in_collection(user_object['id_str'], 'user_demographics') == False:
            user_objects_list_to_detect_demographics.append(user_object)
        else:
            user_object['demographics'] = load_object_from_collection(user_object['id_str'], 'user_demographics')['demographics']
        
    # Preprocess user object for m3inference
    users_demographics_input_list = []
    user_counter = 0 # DEBUG
    user_count = len(user_objects_list_to_detect_demographics) # DEBUG
    for user_object in user_objects_list_to_detect_demographics:
        if document_exists_in_collection(user_object['id_str'], 'user_m3_preprocessed'):
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
        print(f'Preprocess M3 {user_counter} / {user_count}')
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

    db_op_result = save_multiple_documents_to_collection(documents_to_save, 'user_demographics')
    if db_op_result != None:
        print(f'Saved {len(db_op_result.inserted_ids)} user demographics')

    # ----------------------------------
    # Finalize the demographics prediction of each user
    # ----------------------------------
    for user_object in user_objects_list:
        user_object['age_predicted'] = max(user_object['demographics']['age'], key=user_object['demographics']['age'].get)
        user_object['gender_predicted'] = max(user_object['demographics']['gender'], key=user_object['demographics']['gender'].get)
        user_object['org_predicted'] = max(user_object['demographics']['org'], key=user_object['demographics']['org'].get)


    return user_objects_list


def analysis_pipeline_download_tweets(url):
    # if url exist in collection urls, skip
    if DATABASE['internet_archive_urls'].count_documents({'url': url}, limit = 1) >= 1:
        print(f'URL {url} already exists in the database')
        downloaded_tweets_list = list(DATABASE['original_tweets'].find({'downloaded_from': url}))
    else:
        downloaded_tweets_list = download_tweets(url)
        print(f'Downloaded {len(downloaded_tweets_list)} tweets from {url}')
        for tweet_obj in downloaded_tweets_list:
            tweet_obj['downloaded_from'] = url
        # Save the url to the database
        DATABASE['internet_archive_urls'].insert_one({'url': url})

        # Insert all downloaded tweets into MongoDB collection. Set id_str as the primary key - `_id`
        # If the tweet with the same id_str already exists, do not insert it.
        documents_to_insert = [{**tweet_object, '_id': tweet_object['id_str']} for tweet_object in downloaded_tweets_list if DATABASE['original_tweets'].count_documents({'_id': tweet_object['id_str']}, limit = 1) == 0]
        if len(documents_to_insert) > 0:
            db_op_result = DATABASE['original_tweets'].insert_many(documents_to_insert)
            print(f'Inserted {len(db_op_result.inserted_ids)} tweets')

    return downloaded_tweets_list

def analyze_data_by(year, month, day, hour, minute):

    url = get_download_url(year, month, day, hour, minute)
    print(url)

    downloaded_tweets_list = analysis_pipeline_download_tweets(url)
    
    # Analyze the tweet objects that are not cached
    analyzed_tweets, topics_values = analyze_multiple_tweets(downloaded_tweets_list)

    # Analyze the users of the tweets
    user_objects_list = [tweet_object['user'] for tweet_object in downloaded_tweets_list]

    # Analyze the user objects that are not cached
    analyzed_users = analyze_multiple_users(user_objects_list)
