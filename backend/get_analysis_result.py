from mongo_constants import COLLECTION_NAME_REGISTRY, DATABASE


def get_analysis_result(
    tweet_ids: list[str],
    tweet_collection_list=[
        COLLECTION_NAME_REGISTRY["tweet_text_original"],
        COLLECTION_NAME_REGISTRY["tweet_filtered_pre_translation"],
        COLLECTION_NAME_REGISTRY["tweet_translated"],
        COLLECTION_NAME_REGISTRY["tweet_filtered_post_translation"],
        COLLECTION_NAME_REGISTRY["tweet_processed"],
        COLLECTION_NAME_REGISTRY["tweet_sentiment"],
        COLLECTION_NAME_REGISTRY["tweet_topics_lda"],
        COLLECTION_NAME_REGISTRY["tweet_topics_lda_results"],
        COLLECTION_NAME_REGISTRY["tweet_topics_bertopic_arxiv"],
        COLLECTION_NAME_REGISTRY["tweet_topics_cardiffnlp"],
    ],
    user_collection_list=[
        COLLECTION_NAME_REGISTRY["user_location_translated"],
        COLLECTION_NAME_REGISTRY["user_location_coordinates"],
        COLLECTION_NAME_REGISTRY["user_location_country"],
        COLLECTION_NAME_REGISTRY["user_demographics"],
        COLLECTION_NAME_REGISTRY["user_demographics_result"],
        COLLECTION_NAME_REGISTRY["user_m3_preprocessed"],
    ],
) -> list[dict]:
    
    tweet_object_list = DATABASE[COLLECTION_NAME_REGISTRY["original_tweets"]].find({"_id": {"$in": tweet_ids}})
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
