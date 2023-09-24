from mongo_constants import DATABASE, CollectionNames


def get_analysis_result(
    tweet_ids: list[str],
    tweet_collection_list=[
        CollectionNames.tweet_text_original.value,
        CollectionNames.tweet_filtered_pre_translation.value,
        CollectionNames.tweet_translated.value,
        CollectionNames.tweet_filtered_post_translation.value,
        CollectionNames.tweet_processed.value,
        CollectionNames.tweet_sentiment.value,
        CollectionNames.tweet_topics_lda.value,
        CollectionNames.tweet_topics_lda_results.value,
        CollectionNames.tweet_topics_bertopic_arxiv.value,
        CollectionNames.tweet_topics_cardiffnlp.value,
    ],
    user_collection_list=[
        CollectionNames.user_location_translated.value,
        CollectionNames.user_location_coordinates.value,
        CollectionNames.user_location_country.value,
        CollectionNames.user_demographics.value,
        CollectionNames.user_demographics_result.value,
        CollectionNames.user_m3_preprocessed.value,
    ],
) -> list[dict]:
    
    tweet_object_list = DATABASE[CollectionNames.original_tweets.value].find({"_id": {"$in": tweet_ids}})
    tweet_object_list = list(tweet_object_list)

    all_collection_values = {}

    for collection_name in tweet_collection_list + user_collection_list:
        all_collection_values[collection_name] = DATABASE[collection_name].find({"_id": {"$in": tweet_ids}})
        all_collection_values[collection_name] = list(all_collection_values[collection_name])
        all_collection_values[collection_name] = {document["_id"]: document["value"] for document in all_collection_values[collection_name]}

    for tweet_object in tweet_object_list:
        tweet_id = tweet_object["id_str"]
        for collection_name in tweet_collection_list:
            tweet_object[collection_name] = all_collection_values[collection_name].get(tweet_id, None)

        user_object = tweet_object["user"]
        user_id = user_object["id_str"]
        for collection_name in user_collection_list:
            user_object[collection_name] = all_collection_values[collection_name].get(user_id, None)

    return tweet_object_list
