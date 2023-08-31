from workflow import *
import json


def mySource():
    # data = download_tweets(0)
    data = []

    file_path = "data\\test.json"  # Replace with the actual path to your file
    with open(file_path, "r") as json_file:
        for line in json_file:
            data.append((json.loads(line)))

    data = filter_tweets(data)  # output is a list of dict

    # this file will contain all data fields of interest
    filtered_data_full_tweets = save_data_full('data\\full_0.json', data)

    #this file will contain tweets only which have been translated
    data = save_complete_data('data\\data.json', filtered_data_full_tweets)

    print(data)

    tweet_data = []
    for text in data:
        tweet_data.append(text["text_original"])

    keywords = topic_modelling(tweet_data)

    topics = topic_modelling_define_topics(keywords)

    sentiment_analysis_result = sentiment_analysis(tweet_data)

    location_data = save_extracted_location_data('data\\location.json', data)

    age_data = save_extracted_age('data\\age.json', location_data)

    return topics, sentiment_analysis_result


r = mySource()

print("topics: ", r[0], "\nnegative: ", r[1][0], "\tpositive: ", r[1][1], "\tneutral:", r[1][2])
