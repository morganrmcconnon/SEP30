from features import utils
import pandas as pd
from m3inference import M3Twitter
from m3inference.consts import UNKNOWN_LANG, LANGS
from m3inference.utils import transform_jsonl_object_for_m3inference_text_model
from googletrans import Translator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import random
import json

TRANSLATOR = Translator()

data = []

file_path = "data\\tesSM.json"  # Replace with the actual path to your file
with open(file_path, "r") as json_file:
    for line in json_file:
        data.append((json.loads(line)))

users = [d['user'] for d in data]
new_data = []

with open('data\\test_processed_0.json', 'w') as f:
    for tweet in data:
        new_tweet = {}
        new_tweet['lang'] = tweet['lang']
        new_tweet['id_str'] = tweet['id_str']
        new_tweet['text_original'] = utils.clean_tweet_text(utils.get_tweet_text(tweet))
        new_user = {}
        new_user['lang'] = tweet['user']['lang']
        new_user['id'] = tweet['user']['id_str']
        new_user['name'] = tweet['user']['name']
        new_user['screen_name'] = tweet['user']['screen_name']
        new_user['location_original'] = tweet['user']['location']
        new_user['description_original'] = tweet['user']['description']

        new_tweet['user'] = new_user
        new_data.append(new_tweet)

        f.write(json.dumps(new_tweet) + '\n')

with open('test_processed_1.json', 'w') as f:
    for new_tweet in new_data:

        if new_tweet['lang'] != 'en':

            text_translated = TRANSLATOR.translate(new_tweet['text_original'], dest='en')
            new_tweet['text_english'] = text_translated.text
            new_tweet['text_lang_detected'] = text_translated.src

        else:
            new_tweet['text_english'] = new_tweet['text_original']
            new_tweet['text_lang_detected'] = 'en'

        f.write(json.dumps(new_tweet) + '\n')

with open('test_processed_2.json', 'w') as f:
    for new_tweet in new_data:

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

with open('test_processed_2.json', 'w') as f:
    for new_tweet in new_data:

        new_user = new_tweet['user']

        if new_user['lang'] != 'en':
            description_translated = TRANSLATOR.translate(new_user['description_original'], dest='en')
            new_user['description_english'] = description_translated.text
            new_user['description_lang_detected'] = description_translated.src

        f.write(json.dumps(new_tweet) + '\n')
# 12m 35.2s


# %%
with open('test_translated.json', 'w') as f:
    for new_tweet in new_data:
        f.write(json.dumps(new_tweet) + '\n')
# %%
new_data = utils.read_jsonl('test_translated.json')
# %%
for new_tweet in new_data:
    new_user = new_tweet["user"]
    new_user["text_lang_detected"] = new_tweet["text_lang_detected"]
    new_user["text_lang"] = new_tweet["lang"]

new_users = [new_tweet["user"] for new_tweet in new_data]

new_users_dict = {}
for new_user in new_users:
    user_id = new_user["id"]
    if user_id not in new_users_dict:
        new_users_dict[user_id] = {}
        for k, v in new_user.items():
            if k != "id":
                new_users_dict[user_id][k] = [v]
            else:
                new_users_dict[user_id][k] = v
    else:
        for k, v in new_user.items():
            if v not in new_users_dict[user_id][k]:
                new_users_dict[user_id][k].append(v)

new_users = list(new_users_dict.values())
# %%
[user for user in new_users if len(user["name"]) > 1]
# %%
[user for user in new_users if user['lang'][0] != None]
# %%
[user for user in new_users if len(user["location_english"]) != 1]
# %%

geolocator = Nominatim(user_agent="location_detection", timeout=60)

# %%
# Extract the user's location
with open('test_user_location.json', 'w') as f:
    for user in new_users:

        user_location_eng = user['location_english'][0]

        try:
            # Initialize a geocoder
            if user_location_eng:

                location_eng = geolocator.geocode(user_location_eng, timeout=60)

                if location_eng:
                    # Extract the latitude and longitude
                    latitude = location_eng.latitude
                    longitude = location_eng.longitude

                    user['latitude'] = latitude
                    user['longitude'] = longitude

                    # # Print the coordinates
                    # print(f"Latitude: {latitude}, Longitude: {longitude}")
                else:
                    print("[Location not found]", user_location_eng)

        except Exception as e:
            print("[Error]:", str(e))

        f.write(json.dumps(user) + '\n')

# 13m 1.4s
# %%
new_users = utils.read_jsonl('test_user_location.json')
# %%
for user in new_users:
    user["name"] = user["name"][0]
    user["screen_name"] = user["screen_name"][0]
    user["location_english"] = user["location_english"][0]
    user["location_original"] = user["location_original"][0]
    user["location_lang_detected"] = user["location_lang_detected"][0]
    user["description_english"] = user["description_english"][0]
    user["description_original"] = user["description_original"][0]
    user["description_lang_detected"] = user["description_lang_detected"][0]
    if user["description_lang_detected"] in LANGS:
        user["lang"] = user["description_lang_detected"]
        user["description"] = user["description_original"]
    else:
        user["lang"] = 'en'
        user["description"] = user["description_english"]
# %%
m3twitter = M3Twitter(cache_dir="./twitter_cache", use_full_model=False, use_cuda=False, parallel=True)
# %%
users_demographics = m3twitter.infer(new_users)
# 1m 1.3s
# %%
users_demographics_32 = m3twitter.infer(new_users, batch_size=32)
# 1m 1.6s
# %%
for user in new_users:
    user['demographics'] = users_demographics[user['id']]
# %%
with open('test_user_demographics.json', 'w') as f:
    for user in new_users:
        f.write(json.dumps(user) + '\n')
# %%
# Test runtime performace of an analysis on 1 single tweet entry

random_tweet = random.choice(data)

new_tweet = {}
new_tweet['id_str'] = random_tweet['id_str']
new_tweet['lang'] = random_tweet['lang']
new_tweet['text_original'] = utils.clean_tweet_text(utils.get_tweet_text(random_tweet))

new_user = {}
new_user['id'] = random_tweet['user']['id_str']
new_user['name'] = random_tweet['user']['name']
new_user['screen_name'] = random_tweet['user']['screen_name']
new_user['lang'] = random_tweet['user']['lang']
new_user['location_original'] = random_tweet['user']['location']
new_user['description_original'] = random_tweet['user']['description']

new_tweet['user'] = new_user

# if new_tweet['lang'] != 'en':

text_translated = TRANSLATOR.translate(new_tweet['text_original'], dest='en')
new_tweet['text_english'] = text_translated.text
new_tweet['text_lang_detected'] = text_translated.src

# else:
#     new_tweet['text_english'] = new_tweet['text_original']
#     new_tweet['text_lang_detected'] = 'en'

# if new_user['lang'] != 'en':

location_translated = TRANSLATOR.translate(new_user['location_original'], dest='en')
new_user['location_english'] = location_translated.text
new_user['location_lang_detected'] = location_translated.src

description_translated = TRANSLATOR.translate(new_user['description_original'], dest='en')
new_user['description_english'] = description_translated.text
new_user['description_lang_detected'] = description_translated.src

# else:
#     new_user['location_english'] = new_user['location_original']
#     new_user['location_lang_detected'] = 'en'
#     new_user['description_english'] = new_user['description_original']
#     new_user['description_lang_detected'] = 'en'


new_user["text_lang_detected"] = new_tweet["text_lang_detected"]
new_user["text_lang"] = new_tweet["lang"]

user_location_eng = new_user['location_english']

try:
    # Initialize a geocoder
    if user_location_eng:

        location_eng = geolocator.geocode(user_location_eng, timeout=60)

        if location_eng:
            # Extract the latitude and longitude
            latitude = location_eng.latitude
            longitude = location_eng.longitude

            new_user['latitude'] = latitude
            new_user['longitude'] = longitude

            # # Print the coordinates
            # print(f"Latitude: {latitude}, Longitude: {longitude}")
        else:
            print("[Location not found]", user_location_eng)

except Exception as e:
    print("[Error]:", str(e))

if new_user["description_lang_detected"] in LANGS:
    new_user["lang"] = new_user["description_lang_detected"]
    new_user["description"] = new_user["description_original"]
else:
    new_user["lang"] = 'en'
    new_user["description"] = new_user["description_english"]

# 2.4s
# %%

new_users_demographics = m3twitter.infer([new_user])

new_user['demographics'] = new_users_demographics[new_user['id']]
