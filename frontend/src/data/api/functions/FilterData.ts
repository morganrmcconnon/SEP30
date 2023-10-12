import { TweetObject } from "../types/TweetObject";
import { UserObject } from "../types/UserObject";


function filter_tweet_objects_list_by(tweet_objects: Array<TweetObject>, sentiment: string | null, topic: string | null, keyword: string | null) {

    return tweet_objects.filter(tweet_object => {
        const sentiment_predicted = tweet_object.sentiment;
        //const topic_with_the_highest_score = tweet_object.topic_lda.topic_id;
        const associated_keywords = tweet_object.text_processed;
        const original_text = tweet_object.text;
        const text_in_english = tweet_object.text_in_english;
        return (
            (sentiment === null || sentiment_predicted === sentiment) &&
            (topic === null || tweet_object.topic_lda.related_topics.cosine_similarity.includes(topic)) &&
            (keyword === null || associated_keywords.includes(keyword) || original_text.includes(keyword) || text_in_english.includes(keyword))
        );
    });
}

function filter_user_objects_list_by(user_objects: Array<UserObject>, location: string | null, gender: string | null, age: string | null, org: string | null) {

    return user_objects.filter(user_object => {
        const country_code = user_object.country_code;
        const age_predicted = user_object.age;
        const gender_predicted = user_object.gender;
        const org_predicted = user_object.org;
        return (
            (country_code === location || location === null) &&
            (age_predicted === age || age === null) &&
            (gender_predicted === gender || gender === null) &&
            (org_predicted === org || org === null)
        );
    });

}

function filter_tweets_by_users(tweet_objects: Array<TweetObject>, user_objects: Array<UserObject>) {
    const user_ids = user_objects.map(user_object => user_object['id_str']);
    return tweet_objects.filter(tweet_object => user_ids.includes(tweet_object['user']['id_str']));
}

function filter_users_by_tweets(user_objects: Array<UserObject>, tweet_objects: Array<TweetObject>) {
    const user_ids = tweet_objects.map(tweet_object => tweet_object['user']['id_str']);
    return user_objects.filter(user_object => user_ids.includes(user_object['id_str']));
}

function filter_data_by(
    tweet_objects: Array<TweetObject>,
    user_objects: Array<UserObject>,
    sentiment: string | null = null,
    topic: string | null = null,
    keyword: string | null = null,
    location: string | null = null,
    gender: string | null = null,
    age: string | null = null,
    org: string | null = null
) {

    let new_tweet_objects = filter_tweet_objects_list_by(tweet_objects, sentiment, topic, keyword);


    let new_user_objects = filter_users_by_tweets(user_objects, new_tweet_objects);


    new_user_objects = filter_user_objects_list_by(new_user_objects, location, gender, age, org);


    new_tweet_objects = filter_tweets_by_users(new_tweet_objects, new_user_objects);

    return {
        new_tweet_objects,
        new_user_objects
    };
}

export { filter_data_by, filter_tweet_objects_list_by, filter_user_objects_list_by, filter_tweets_by_users, filter_users_by_tweets };