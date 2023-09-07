from features import utils
import pandas as pd
from m3inference import M3Twitter
from m3inference.consts import UNKNOWN_LANG, LANGS
from googletrans import Translator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import random
import json


def save_files_full(file_path, data, users):
    new_data = []
    with open(file_path, 'w') as f:
        for tweet in data:
            new_tweet = {'lang': tweet['lang'],
                         'id_str': tweet['id_str'],
                         'text_original': utils.get_tweet_text(tweet)}  # not cleaned yet

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


def save_translated_tweets(file_path, json_data):
    TRANSLATOR = Translator()
    with open(file_path, 'w') as f:
        for new_tweet in json_data:

            if new_tweet['lang'] != 'en':

                text_translated = TRANSLATOR.translate(new_tweet['text_original'], dest='en')
                new_tweet['text_english'] = text_translated.text
                new_tweet['text_lang_detected'] = text_translated.src

            else:
                new_tweet['text_english'] = new_tweet['text_original']
                new_tweet['text_lang_detected'] = 'en'

            f.write(json.dumps(new_tweet) + '\n')


def save_translated_users(file_path, json_data):
    TRANSLATOR = Translator()
    with open(file_path, 'w') as f:
        for new_tweet in json_data:

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

            f.write(json.dumps(new_tweet) + '\n')

def save_tweets_only(file_path, data):
    with open('test_translated.json', 'w') as f:
        for new_tweet in data:
            f.write(json.dumps(new_tweet) + '\n')


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




