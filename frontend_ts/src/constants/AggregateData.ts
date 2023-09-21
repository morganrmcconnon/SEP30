import { SentimentData, TweetObject } from "./TweetObjectTypes";
import { AgeGroupData, GenderData, OrgData, UserObject } from "./UserObjectTypes";

function aggregate_tweet_objects_list(tweet_objects: Array<TweetObject>) {
  const sentiment_count: SentimentData = {
    "positive": 0,
    "negative": 0,
    "neutral": 0
  };

  const female_sentiment = { positive: 0, neutral: 0, negative: 0 };
  const male_sentiment = { positive: 0, neutral: 0, negative: 0 };

  const topic_count: Record<string, number> = {};

  const keyword_count: Record<string, number> = {};

  const keyword_pairs_count: Record<string, number> = {};

  tweet_objects.forEach(tweet_object => {
    const text_analyzed = tweet_object['text_analyzed'];
    const sentiment_predicted = text_analyzed['sentiment_predicted'];
    const topic_with_the_highest_score = text_analyzed['topic_with_the_highest_score'];
    const associated_keywords = text_analyzed['associated_keywords'];

    sentiment_count[sentiment_predicted] += 1;
    topic_count[topic_with_the_highest_score] = (topic_count[topic_with_the_highest_score] || 0) + 1;
    associated_keywords.forEach(keyword => {
      keyword_count[keyword] = (keyword_count[keyword] || 0) + 1;
    });


    associated_keywords.forEach(keyword1 => {
      associated_keywords.forEach(keyword2 => {
        if (keyword1 !== keyword2) {
          const keyword_pair = [keyword1, keyword2].sort();
          const smaller_keyword = keyword_pair[0];
          const bigger_keyword = keyword_pair[1];
          const keywordsPair = `${smaller_keyword},${bigger_keyword}`;
          keyword_pairs_count[keywordsPair] = (keyword_pairs_count[keywordsPair] || 0) + 1;
        }
      });
    });

    const user = tweet_object['user'];

    if (user.gender_predicted == "female") {
      if (text_analyzed.sentiment_predicted == "positive") {
        female_sentiment.positive++
      } else if (text_analyzed.sentiment_predicted == "neutral") {
        female_sentiment.neutral++
      } else if (text_analyzed.sentiment_predicted == "negative") {
        female_sentiment.negative++
      }
    } else {
      if (text_analyzed.sentiment_predicted == "positive") {
        male_sentiment.positive++
      } else if (text_analyzed.sentiment_predicted == "neutral") {
        male_sentiment.neutral++
      } else if (text_analyzed.sentiment_predicted == "negative") {
        male_sentiment.negative++
      }
    }
  });

  const keywordsPairsArray = Object.entries(keyword_pairs_count).map(([keywordsPair, count]) => {
    return { keywords: keywordsPair.split(','), count };
  });

  return {
    female_sentiment,
    male_sentiment,
    sentiment_count,
    topic_count,
    keyword_count,
    keywordsPairsArray
  };
}


function aggregate_user_objects_list(user_objects: Array<UserObject>) {

  const countries_count: Record<string, number> = {};
  const age_groups_count: AgeGroupData = { "<=18": 0, "19-29": 0, "30-39": 0, ">=40": 0 };
  const genders_count: GenderData = { "female": 0, "male": 0 };
  const org_count: OrgData = { "is-org": 0, "non-org": 0 };

  user_objects.forEach(user_object => {
    const country_code = user_object["location_analyzed"]["country_code"];
    const age_predicted = user_object["age_predicted"];
    const gender_predicted = user_object["gender_predicted"];
    const org_predicted = user_object["org_predicted"];

    countries_count[country_code] = (countries_count[country_code] || 0) + 1;
    age_groups_count[age_predicted] += 1;
    genders_count[gender_predicted] += 1;
    org_count[org_predicted] += 1;

  });

  return {
    countries_count,
    age_groups_count,
    genders_count,
    org_count
  };
}

function aggregate_data(tweet_objects: Array<TweetObject>, user_objects: Array<UserObject>) {
  const aggregated_tweet_objects = aggregate_tweet_objects_list(tweet_objects);
  const aggregated_user_objects = aggregate_user_objects_list(user_objects);
  return {
    ...aggregated_tweet_objects,
    ...aggregated_user_objects
  };
}

export { aggregate_data, aggregate_tweet_objects_list, aggregate_user_objects_list };