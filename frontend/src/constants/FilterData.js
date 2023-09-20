function filter_tweet_objects_list_by(tweet_objects, sentiment = false, topic = false, keyword = false) {
    
    return tweet_objects.filter(tweet_object => {
        const text_analyzed = tweet_object['text_analyzed'];
        const sentiment_predicted = text_analyzed['sentiment_predicted'];
        const topic_with_the_highest_score = text_analyzed['topic_with_the_highest_score'];
        const associated_keywords = text_analyzed['associated_keywords'];
        const original_text = text_analyzed['original'];
        const text_in_english = text_analyzed['in_english'];
        return (
            (sentiment == false || sentiment_predicted === sentiment) &&
            (topic == false || topic_with_the_highest_score === topic) &&
            (keyword == false || associated_keywords.includes(keyword) || original_text.includes(keyword) || text_in_english.includes(keyword))
        );
    });
}

function filter_user_objects_list_by(user_objects, location = false, gender = false, age = false, org = false) {

    return user_objects.filter(user_object => {
        const country_code = user_object["location_analyzed"]["country_code"];
        const age_predicted = user_object["age_predicted"];
        const gender_predicted = user_object["gender_predicted"];
        const org_predicted = user_object["org_predicted"];
        return (
            (country_code === location || location == false) &&
            (age_predicted === age || age == false) &&
            (gender_predicted === gender || gender == false) &&
            (org_predicted === org || org == false)
        );
    });

}

function filter_tweets_by_users(tweet_objects, user_objects) {
    const user_ids = user_objects.map(user_object => user_object['id_str']);
    return tweet_objects.filter(tweet_object => user_ids.includes(tweet_object['user']['id_str']));
}

function filter_users_by_tweets(user_objects, tweet_objects) {
    const user_ids = tweet_objects.map(tweet_object => tweet_object['user']['id_str']);
    return user_objects.filter(user_object => user_ids.includes(user_object['id_str']));
}

function filter_data_by(tweet_objects, user_objects, sentiment = false, topic = false, keyword = false, location = false, gender = false, age = false, org = false) {
    
    let new_tweet_objects = filter_tweet_objects_list_by(tweet_objects, sentiment, topic, keyword);

    console.log("new_tweet_objects");
    console.log(new_tweet_objects);

    let new_user_objects = filter_users_by_tweets(user_objects, new_tweet_objects);

    console.log("new_user_objects");
    console.log(new_user_objects);

    new_user_objects = filter_user_objects_list_by(new_user_objects, location, gender, age, org);

    console.log("new_user_objects");
    console.log(new_user_objects);

    new_tweet_objects = filter_tweets_by_users(new_tweet_objects, new_user_objects);
    console.log("new_tweet_objects");
    console.log(new_tweet_objects);

    return {
        new_tweet_objects,
        new_user_objects
    };
}

export { filter_data_by, filter_tweet_objects_list_by, filter_user_objects_list_by, filter_tweets_by_users, filter_users_by_tweets };