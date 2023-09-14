from features import utils
import pandas as pd
from m3inference import M3Twitter
from m3inference.consts import UNKNOWN_LANG, LANGS
from googletrans import Translator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import random
import json


def extra_users_location(file_path, data):
    output = []
    for new_tweet in data:
        new_user = new_tweet["user"]
        new_user["text_lang_detected"] = new_tweet["text_lang_detected"]
        new_user["text_lang"] = new_tweet["lang"]

    new_users = [new_tweet["user"] for new_tweet in data]

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

    geolocator = Nominatim(user_agent="location_detection", timeout=60)

    # %%
    # Extract the user's location
    with open(file_path, 'w') as f:
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

            output.append(user)
            f.write(json.dumps(user) + '\n')
        return output

def extract_age_data(file_path, data):
    for user in data:
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

    m3twitter = M3Twitter(cache_dir="./twitter_cache", use_full_model=False, use_cuda=False, parallel=True)
    users_demographics = m3twitter.infer(data)
    users_demographics_32 = m3twitter.infer(data, batch_size=32)

    for user in data:
        user['demographics'] = users_demographics[user['id']]

    output = []
    with open(file_path, 'w') as f:
        for user in data:
            output.append(user)
            f.write(json.dumps(user) + '\n')
    return output
