from features import sentiment_analysis_with_roberta
from features.tweets_downloader import *
from features.spacy_matcher import *
from features.topic_modelling import *
from features.save_files import *
from features.demographic import *

def download_tweets(date):
    data = get_tweets(2022, 11, day=1, hour=0, minute=0)

    # 9.6s - 17.9s

    data = data[list(data.keys())[0]]

    json_data = data
    return json_data


def cleanse_tweet(tweet):
    return tweet


def translate_tweet(tweet):
    return tweet


def filter_tweets(json_data):
    '''Select only the tweets related to mental health'''
    filter_data = filter_tweet(json_data)
    print(filter_data)
    return filter_data


def sentiment_analysis(tweet_data):
    n, p, neutral = 0, 0, 0
    for tweet in tweet_data:
        sentiment_result, confidence_probabilities = sentiment_analysis_with_roberta.classify_sentiment(text=tweet)
        r = max(confidence_probabilities)
        print(r)
        if r == 'negative':
            n += 1
        elif r == 'positive':
            p += 1
        else:
            neutral += 1
    return n, p, neutral


def topic_modelling(tweet_data):
    return process_topic_modelling(tweet_data)


def topic_modelling_define_topics(keywords):
    return define_topics(keywords)


def age_identification(json_data):
    return json_data


def gender_identification(json_data):
    return json_data


def location_identification(json_data):
    return json_data


def save_data_full(file_path, data):
    users = [d['user'] for d in data]
    return save_files_full(file_path, data, users)


def save_translated_tweet(file_path, data):
    save_translated_tweets(file_path, data)


def save_translated_user(file_path, data):
    save_translated_users(file_path, data)


def save_translated_tweet_only(file_path, data):
    save_tweets_only(file_path, data)


def save_complete_data(file_path, data):
    return save_complete_processed_data(file_path, data)

def save_extracted_location_data(file_path, data):
    return extra_users_location(file_path, data)

def save_extracted_age(file_path, data):
    return extract_age_data(file_path, data)