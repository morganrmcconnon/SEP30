from flask import Flask, request, jsonify
from datetime import datetime
import time
import os
import json

from components.constants import CollectionNames, DATABASE
from components.analyze_tweets.translate_text import detect_and_translate_language
from components.analyze_tweets.spacy_matcher import create_matcher_model, text_is_related_to_mental_health
from components.analyze_tweets.sentiment_vader import check_sentiment
from components.analyze_tweets.sentiment_analysis import classify_sentiment
from components.analyze_tweets.topic_bertopic_arxiv import BERTOPIC_ARXIV_TOPIC_MODEL, detect_topics_bertopic_arxiv
from components.analyze_tweets.topic_cardiffnlp_tweet_topic import detect_topic_cardiffnlp_tweet_topic
from components.analyze_tweets.topic_modelling import apply_lda_model, get_keywords_of_topic_model, tokenize_lemmatize_and_remove_stopwords, get_similarity_scores, get_topics_distributions
from components.analyze_tweets.topic_lda_load_pretrained import load_pretrained_model
from components.analyze_tweets.detect_demographics import detect_demographics, preprocess_user_object_for_m3inference
from components.analyze_tweets.detect_coordinates import detect_coordinates
from components.analyze_tweets.detect_polygon_geojson import detect_geojson_ploygon



CURRENT_DIR = os.path.dirname(__file__)
CACHE_FOLDER = os.path.join(CURRENT_DIR, "cache")
# A static folder for storing static files
CACHE_STATIC_FOLDER = os.path.join(CURRENT_DIR, "cache_static")
DB_FOLDER = os.path.join(CURRENT_DIR, "db_temp")
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)
if not os.path.exists(CACHE_STATIC_FOLDER):
    os.makedirs(CACHE_STATIC_FOLDER)
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
TOPIC_VALUES_FILE = os.path.join(CURRENT_DIR, "services/topic_model/topics.json")


SPACY_MATCHER_OBJ, SPACY_NLP_OBJ = create_matcher_model()

BERTOPIC_NAME_MAP = BERTOPIC_ARXIV_TOPIC_MODEL.get_topic_info().set_index('Topic')['Name'].to_dict()



LDA_PRETRAINED_MODEL, LDA_TOPICS_REPRESENTATIONS = load_pretrained_model()

LDA_PRETRAINED_MODEL_ID = "0"

LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS = get_topics_distributions(LDA_PRETRAINED_MODEL)

KEYWORDS_OF_TOPIC_MODEL = get_keywords_of_topic_model(LDA_TOPICS_REPRESENTATIONS)



app = Flask(__name__, static_folder=f"../frontend/dist", static_url_path="/")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/")
def hello_world():
    return "<p>Hello, there!</p>"


@app.route("/api/example_endpoint_get", methods=["GET"])
def endpoint_test_example_get_data():
    # Return content from server
    return {"greeting": "Hello!!!!!!"}


@app.route("/api/time")
@app.route("/backend/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/api/analysis/translate", methods=["POST"])
def translate_text():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    text_en, src, _, _ = detect_and_translate_language(text)
    return {"in_english": text_en, "lang_detected": src}


@app.route("/api/analysis/text/processed", methods=["POST"])
def process_text():
    data = request.get_json()
    text = data["text"]
    return {"text_processed": tokenize_lemmatize_and_remove_stopwords(text) }


@app.route("/api/analysis/filter/spacy", methods=["POST"])
def filter_spacy():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    is_related = text_is_related_to_mental_health(text, SPACY_MATCHER_OBJ, SPACY_NLP_OBJ)
    return { "is_related": is_related }


@app.route("/api/sentiment_vader", methods=["POST"])
@app.route("/api/analysis/sentiment/vader", methods=["POST"])
def check_sentiment_with_vader():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    compound_score, sentiment_label = check_sentiment(text)
    return {"compound_score": compound_score, "sentiment_label": sentiment_label}


@app.route("/api/sentiment", methods=["POST"])
@app.route("/api/analysis/sentiment/roberta", methods=["POST"])
def check_sentiment_with_roberta():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    # Analyze the sentiment of text
    sentiment_result, confidence_probabilities = classify_sentiment(text=text)
    return {
        "sentiment_result": sentiment_result,
        "confidence_probabilities": confidence_probabilities,
    }


@app.route("/api/analysis/topic/bertaxiv", methods=["POST"])
def topic_inference_with_bertarxiv():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    topics_detected_list, probs_detected_list = detect_topics_bertopic_arxiv([text])
    topic_id = int(topics_detected_list[0])
    probability = float(probs_detected_list[0])
    topic_name = BERTOPIC_NAME_MAP[topic_id]
    return {
        "topic_id": topic_id,
        "topic_name": topic_name,
        "probability": probability,
    }


@app.route("/api/analysis/topic/cardiffnlp", methods=["POST"])
def topic_inference_with_cardiffnlp():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    text = data["text"]
    topics = detect_topic_cardiffnlp_tweet_topic(text)
    topic = max(topics, key=lambda x: x["topic_score"])
    return {
        'topic_id': topic['topic_id'],
        'topic_name': topic['topic_name'],
        'topic_score': topic['topic_score'],
    }


@app.route("/api/analysis/topic/lda", methods=["POST"])
def topic_inference_with_lda():
    
    data = request.get_json()
    text = data["text"]
    
    # Apply LDA model to detect the topics of the text
    topics_distribution = apply_lda_model(text, LDA_PRETRAINED_MODEL)
    highest_score_topic = max(topics_distribution, key=lambda x: x[1])
    
    
    # Calculate the similarity scores of the topic labels to the tweet
    related_topics_cossim = get_similarity_scores(LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS, topics_distribution, method="cossim")
    related_topics_cossim.sort(key=lambda x: x[1], reverse=True)    
    
    cosine_similarity_benchmark = 0.5
    related_topics_cossim = [related_topics_cossim[0][0]] + [topic[0] for topic in related_topics_cossim[1:5] if topic[1] > cosine_similarity_benchmark]
    
    related_topics_hellinger = get_similarity_scores(LDA_DEFAULT_MODEL_LABELS_TOPICS_DISTRIBUTIONS, topics_distribution, method="hellinger")
    related_topics_hellinger.sort(key=lambda x: x[1], reverse=False)

    hellinger_distance_benchmark = 0.5
    related_topics_hellinger = [related_topics_hellinger[0][0]] + [topic[0] for topic in related_topics_hellinger[1:5] if topic[1] < hellinger_distance_benchmark]

    associated_keywords = [[keywords_of_topic ,[keyword for keyword in keywords_of_topic if keyword in text]] for keywords_of_topic in KEYWORDS_OF_TOPIC_MODEL.values()]


    return {
        # 'topics_distribution': topics_distribution,
        'highest_score_topic': highest_score_topic[0],
        'highest_score_topic_probability': highest_score_topic[1],
        'related_topics': {
            'cosine_similarity': related_topics_cossim,
            'hellinger_distance': related_topics_hellinger, 
        },
        'associated_keywords': associated_keywords
    }



@app.route("/api/analysis/user/location", methods=["POST"])
def detect_user_location():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    location_description = data["text"]
    # Detect the language of the text
    location_in_english, lang_detected, _, _ = detect_and_translate_language(location_description)


    # Get the coordinates of the user
    try:
        coordinates = detect_coordinates(location_description, lang_detected)
    except:
        coordinates = detect_coordinates(location_in_english)
    if coordinates == None:
        latitude = None
        longitude = None
    else:
        latitude = coordinates[0]
        longitude = coordinates[1]


    if latitude == None or longitude == None:
        return {
            'latitude': latitude,
            'longitude': longitude,
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
        'latitude': latitude,
        'longitude': longitude,
        'country_name': country_name,
        'country_code': country_code
    }


@app.route("/api/analysis/user/demographics/m3inference", methods=["POST"])
def detect_user_demographic():
    # Get content from client, process it on server, and return it
    data = request.get_json()
    user_id = '0'
    user_object = {
        'id_str': user_id,
        'name': data["name"],
        'screen_name': data["screen_name"],
        'description': data["description"],
        'lang': data["lang"]
    }
    user_object_preprocessed = preprocess_user_object_for_m3inference(user_object, 
                                                                        id_key='id_str', 
                                                                        name_key='name',
                                                                        screen_name_key='screen_name',
                                                                        description_key='description',
                                                                        lang_key='lang',
                                                                        use_translator_if_necessary=True)
    demographics = detect_demographics([user_object_preprocessed])
    user_demographics = demographics[user_id]
    age_predicted = max(user_demographics['age'], key=user_demographics['age'].get)
    gender_predicted = max(user_demographics['gender'], key=user_demographics['gender'].get)
    org_predicted = max(user_demographics['org'], key=user_demographics['org'].get)
    return {
        'age_predicted': age_predicted,
        'gender_predicted': gender_predicted,
        'org_predicted': org_predicted
    }


@app.route("/api/analyze_multiple_tweet_cached")
@app.route("/backend/get_analyzed_data_cached", methods=["GET"])
def get_analyzed_data_cached():
    # Return cached analyzed result

    cached_analysis_result = json.load(open(os.path.join(CACHE_FOLDER, "cache_analysis_result.json"), "r"))

    return cached_analysis_result

@app.route("/api/analyze_multiple_tweet_cached_static")
@app.route("/backend/get_analyzed_data_cached_static", methods=["GET"])
@app.route("/backend/get_cached_static", methods=["GET"])
def get_analyzed_data_cached_static():
    # Return cached analyzed result from static folder

    cached_analysis_result = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_analysis_result.json"), "r"))

    return cached_analysis_result



@app.route("/api/analyze_multiple_tweet")
@app.route("/backend/get_analyzed_data", methods=["GET"])
def get_analyze_multiple_tweet_data():
    # Return content from server

    cached_analysis_result = json.load(open(os.path.join(CACHE_STATIC_FOLDER, "cache_analysis_result.json"), "r"))

    end_analysis_at = cached_analysis_result['analysis_timestamps']['end_analysis_at']

    print(end_analysis_at)

    # If the cached data is older than 10 minutes ago, re-analyze the tweets
    if time.time() - end_analysis_at > 6000:
        # return get_analyzed_data_full()
        return get_analyzed_data_cached()
        
    else:
        return get_analyzed_data_cached()

@app.route("/api/data", methods=["POST"])
@app.route("/backend/data", methods=["POST"])
def data_select_tweets_by_timestamp_ms_range():
    data = request.get_json()
    start_timestamp_ms = str(data['start'])
    end_timestamp_ms = str(data['end'])


    # Query MongoDB collection to select tweet IDs based on timestamp range

    total_tweets_count = DATABASE['analyzed_tweets'].count_documents({
                "timestamp_ms": {"$gte": start_timestamp_ms, "$lte": end_timestamp_ms}
            })
    
    print(total_tweets_count)
    
    query_filter = {
        "timestamp_ms": {"$gte": start_timestamp_ms, "$lte": end_timestamp_ms},
        # filter tweets that are not mental health related
        "$or": [
            { 'topic_bert_arxiv.topic_id': 55 },
            { 'spacy_match.in_english': True },
            { 'spacy_match.original': True }
        ]
    }

    related_tweets_analyzed = DATABASE['analyzed_tweets'].find(query_filter)
    
    related_tweets_analyzed = list(related_tweets_analyzed)

    related_tweets_count = len(related_tweets_analyzed)

    # Temporary get the first tweet's LDA model ID
    lda_model_id = related_tweets_analyzed[0]['topic_lda']['model_id']

    lda_topic_model_values = DATABASE[CollectionNames.topic_models_lda.value].find_one({'_id': lda_model_id})

    response_object = {
        "aggregate_results": {
            "total_tweets_count": total_tweets_count,
            "related_tweets_count": related_tweets_count,
        },
        "lda_topic_model": lda_topic_model_values,
        "tweet_objects": related_tweets_analyzed
    }

    
    return jsonify(response_object)




#Additional MongoDB functionalities
@app.route("/api/select_analyzed_tweets", methods=["GET"])
def select_analyzed_tweets():
    keyword = request.args.get('keyword')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Convert date strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Query MongoDB collection to select analyzed tweets based on keyword and date range
    selected_tweets = DATABASE['analyzed_tweets'].find({
        'text': {'$regex': keyword, '$options': 'i'},  # Case-insensitive search
        'created_at': {'$gte': start_datetime, '$lte': end_datetime}
    })
    
    # Convert the MongoDB cursor to a list of dictionaries
    selected_tweets_list = list(selected_tweets)
    
    return jsonify(selected_tweets_list)

@app.route("/api/select_tweet_ids_by_date_range", methods=["GET"])
def select_tweet_ids_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Convert date strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Query MongoDB collection to select tweet IDs based on date range
    selected_tweet_ids = DATABASE['analyzed_tweets'].find({
        'created_at': {'$gte': start_datetime, '$lte': end_datetime}
    }).distinct('id_str')  # Get distinct tweet IDs
    
    return jsonify(selected_tweet_ids)


@app.route("/api/select_tweets_by_timestamp_ms", methods=["GET"])
@app.route("/backend/select_tweets_by_timestamp_ms", methods=["GET"])
def select_tweets_by_timestamp_ms_range():
    start_timestamp_ms = request.args.get('start', type=str)
    end_timestamp_ms = request.args.get('end', type=str)
    default_timestamp_ms = str(int(datetime(year=2022, month=10, day=8, hour=12, minute=0).timestamp() * 1000))
    if start_timestamp_ms is None:
        start_timestamp_ms = default_timestamp_ms
    if end_timestamp_ms is None:
        end_timestamp_ms = default_timestamp_ms
    if (not start_timestamp_ms.isdigit()) or (not end_timestamp_ms.isdigit()):
        return jsonify([])
    if len(start_timestamp_ms) != 13 or len(end_timestamp_ms) != 13:
        return jsonify([])
    if start_timestamp_ms > end_timestamp_ms:
        return jsonify([])
    
    
    print(start_timestamp_ms, end_timestamp_ms)
    # Query MongoDB collection to select tweet IDs based on timestamp range
    # Join 2 collections, original_tweets and analyzed_tweets


    total_tweets_count = DATABASE['analyzed_tweets'].count_documents({
                "timestamp_ms": {"$gte": start_timestamp_ms, "$lte": end_timestamp_ms}
            })
    
    query_filter = {
        "timestamp_ms": {"$gte": start_timestamp_ms, "$lte": end_timestamp_ms},
        # filter tweets that are not mental health related
        "$or": [
            { 'topic_bert_arxiv.topic_id': 55 },
            { 'spacy_match.in_english': True },
            { 'spacy_match.original': True }
        ]
    }

    related_tweets_analyzed = DATABASE['analyzed_tweets'].find(query_filter)
    
    related_tweets_analyzed = list(related_tweets_analyzed)

    related_tweets_count = len(related_tweets_analyzed)

    # Temporary get the first tweet's LDA model ID
    lda_model_id = related_tweets_analyzed[0]['topic_lda']['model_id']

    lda_topic_model_values = DATABASE[CollectionNames.topic_models_lda.value].find_one({'_id': lda_model_id})

    response_object = {
        "aggregate_results": {
            "total_tweets_count": total_tweets_count,
            "related_tweets_count": related_tweets_count,
        },
        "lda_topic_model": lda_topic_model_values,
        "tweet_objects": related_tweets_analyzed
    }

    with open(os.path.join(CACHE_FOLDER, 'backend_response.json'), 'w') as f:
        json.dump(response_object, f)
    
    return jsonify(response_object)

@app.route("/api/get_cached", methods=["GET"])
@app.route("/backend/get_cached", methods=["GET"])
def get_cached():
    # Return cached analyzed result from static folder

    cached_analysis_result = json.load(open(os.path.join(CACHE_FOLDER, "backend_response.json"), "r"))

    return cached_analysis_result


@app.route("/api/get_analyzed_data_by_tweet_ids", methods=["POST"])
def get_analyzed_data_by_tweet_ids():
    # Implement the logic to check if analysis results are cached for the given tweet IDs
    # If cached, retrieve and return the cached analysis results
    # If not cached, analyze the list of tweets and cache the results
    
    tweet_ids_to_analyze = request.json.get('tweet_ids')
    cached_analysis_results = []
    uncached_tweet_ids = []
    
    # Check which tweet IDs are already cached
    for tweet_id in tweet_ids_to_analyze:
        cached_result = DATABASE['analyzed_tweets'].find_one({'_id': tweet_id})
        if cached_result:
            cached_analysis_results.append(cached_result)
        else:
            uncached_tweet_ids.append(tweet_id)
    
    # Analyze the uncached tweet IDs
    if uncached_tweet_ids:
        # Retrieve uncached tweets from MongoDB
        uncached_tweets = DATABASE['original_tweets'].find({'id_str': {'$in': uncached_tweet_ids}})
        
        # DEBUG
        # For now, we will comment this out to save time when starting the Flask app. 
        # There is a possibility that we are not going to analyze tweets in the Flask backend.
        #  
        # Analyze the uncached tweets
        # analyzed_results = analyze_multiple_tweets(list(uncached_tweets), filter_after_translating=True)
        
        # # Cache the analyzed results in MongoDB
        # documents_to_insert = [{**result, '_id': result['id_str']} for result in analyzed_results]
        # if documents_to_insert:
        #     db_op_result = C_ANALYZED_TWEETS.insert_many(documents_to_insert)
        #     print(f'Saved {len(db_op_result.inserted_ids)} analyzed tweets')
        
        # cached_analysis_results.extend(analyzed_results)
    
    return jsonify(cached_analysis_results)
