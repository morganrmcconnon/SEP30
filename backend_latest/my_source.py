import json
import os
from googletrans import Translator

from services.analyze_tweets.tweet_text import get_tweet_text
from services.analyze_tweets.spacy_matcher import filter_tweet
from services.analyze_tweets.topic_modelling import topic_modelling
from services.analyze_tweets.define_topics import define_topics
from services.analyze_tweets.sentiment_analysis import classify_sentiment



def save_files_full(file_path, data, users):
    new_data = []
    with open(file_path, 'w') as f:
        for tweet in data:
            new_tweet = {'lang': tweet['lang'],
                         'id_str': tweet['id_str'],
                         'text_original': get_tweet_text(tweet)}  # not cleaned yet

            new_user = {'lang': tweet['user']['lang'],
                        'id': tweet['user']['id_str'],
                        'name': tweet['user']['name'],
                        'screen_name': tweet['user']['screen_name'],
                        'location_original': tweet['user']['location'],
                        'description_original': tweet['user']['description']}

            new_tweet['user'] = new_user
            new_data.append(new_tweet)

            f.write(json.dumps(new_tweet) + '\n')
    return new_data


def save_complete_processed_data(file_path, data):
    TRANSLATOR = Translator()

    with open('test_translated.json', 'w') as f:
        new_data = []
        for new_tweet in data:
            if new_tweet['lang'] != 'en':

                text_translated = TRANSLATOR.translate(new_tweet['text_original'], dest='en')
                new_tweet['text_english'] = text_translated.text
                new_tweet['text_lang_detected'] = text_translated.src

            else:
                new_tweet['text_english'] = new_tweet['text_original']
                new_tweet['text_lang_detected'] = 'en'

            new_user = new_tweet['user']

            if new_user['lang'] != 'en':

                location_translated = TRANSLATOR.translate(new_user['location_original'], dest='en')

                new_user['location_english'] = location_translated.text
                new_user['location_lang_detected'] = location_translated.src

            else:
                new_user['location_english'] = new_user['location_original']
                new_user['location_lang_detected'] = 'en'
                new_user['description_english'] = new_user['description_original']
                new_user['description_lang_detected'] = 'en'

            new_user = new_tweet['user']

            if new_user['lang'] != 'en':
                description_translated = TRANSLATOR.translate(new_user['description_original'], dest='en')
                new_user['description_english'] = description_translated.text
                new_user['description_lang_detected'] = description_translated.src

            new_data.append(new_tweet)
            f.write(json.dumps(new_tweet) + '\n')
        return new_data




def sentiment_analysis(tweet_data):
    n, p, neutral = 0, 0, 0
    for tweet in tweet_data:
        sentiment_result, confidence_probabilities = classify_sentiment(text=tweet)
        r = max(confidence_probabilities)
        print(r)
        if r == 'negative':
            n += 1
        elif r == 'positive':
            p += 1
        else:
            neutral += 1
    return n, p, neutral



def save_data_full(file_path, data):
    users = [d['user'] for d in data]
    return save_files_full(file_path, data, users)



def mySource():
    # data = download_tweets(0)
    # return {2,3}, [2,3,1]
    data = []


    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "data", "test.json")
    with open(file_path, "r") as json_file:
        for line in json_file:
            data.append((json.loads(line)))

    data = filter_tweet(data)  # output is a list of dict

    # this file will contain all data fields of interest
    filtered_data_full_tweets = save_data_full('data\\full_0.json', data)

    # this file will contain tweets only which have been translated
    data = save_complete_processed_data('data\\data.json', filtered_data_full_tweets)

    print(data)

    tweet_data = []
    for text in data:
        tweet_data.append(text["text_original"])

    keywords = topic_modelling(tweet_data)

    topics = define_topics(keywords)

    sentiment_analysis_result = sentiment_analysis(tweet_data)

    # location_data = save_extracted_location_data('data\\location.json', data)

    # age_data = save_extracted_age('data\\age.json', location_data)

    return topics, sentiment_analysis_result
