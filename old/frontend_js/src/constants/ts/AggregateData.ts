import TweetObject from "./TweetObject";
import UserObject from "./UserObject";

function feature_extract_tweet(tweet: TweetObject) {
  return {
    "id": tweet.id,
    "id_str": tweet.id_str,
    "created_at": tweet.created_at,
    "timestamp_ms": tweet.timestamp_ms,
    "lang": tweet.lang,
    "text_analyzed": tweet.text_analyzed,
    "user_id": tweet.user.id_str,
    "topics": tweet.text_analyzed.topics,
    "associated_keywords": tweet.text_analyzed.associated_keywords,
    // get the entry with the highest probability
    "sentiment_prediction" : Object.keys(tweet.text_analyzed.sentiment.confidence_probabilities).reduce((a, b) => tweet.text_analyzed.sentiment.confidence_probabilities[a] > tweet.text_analyzed.sentiment.confidence_probabilities[b] ? a : b),
    "topic_prediction" : tweet.text_analyzed.topics.reduce((a, b) => a[1] > b[1] ? a : b)[0],
    // include the following fields if you want
    "text_original": tweet.text_analyzed.original,
    "text_lang_detected": tweet.text_analyzed.lang_detected,
    "text_processed": tweet.text_analyzed.processed,
    "sentiment_result": tweet.text_analyzed.sentiment.result,
    "sentiment_analysis_confidence_probability_of_negative": tweet.text_analyzed.sentiment.confidence_probabilities.negative,
    "sentiment_analysis_confidence_probability_of_positive": tweet.text_analyzed.sentiment.confidence_probabilities.positive,
    "sentiment_analysis_confidence_probability_of_neutral": tweet.text_analyzed.sentiment.confidence_probabilities.neutral,
  };
}

function feature_extract_user(user: UserObject) {
  return {
    "id": user.id,
    "id_str": user.id_str,
    "name": user.name,
    "screen_name": user.screen_name,
    "location": user.location,
    "description": user.description,
    "lang": user.lang,
    "location_analyzed": user.location_analyzed,
    "demographics": user.demographics,
    // get the entry with the highest probability
    "gender_prediction" : Object.keys(user.demographics.gender).reduce((a, b) => user.demographics.gender[a] > user.demographics.gender[b] ? a : b),
    "age_prediction" : Object.keys(user.demographics.age).reduce((a, b) => user.demographics.age[a] > user.demographics.age[b] ? a : b),
    "org_prediction" : Object.keys(user.demographics.org).reduce((a, b) => user.demographics.org[a] > user.demographics.org[b] ? a : b),
    // include the following fields if you want
    "location_description_in_english": user.location_analyzed.in_english,
    "location_lang_detected": user.location_analyzed.lang_detected,
    "latitude": user.location_analyzed.latitude,
    "longitude": user.location_analyzed.longitude,
    "location_analyzed_country_name": user.location_analyzed.country_name,
    "location_analyzed_country_code": user.location_analyzed.country_code,
    // include the following fields if you want
    "gender_confidence_probability_of_male":  user.demographics.gender.male,
    "gender_confidence_probability_of_female":  user.demographics.gender.female,
    "age_confidence_probability_of_<=18":  user.demographics.age["<=18"],
    "age_confidence_probability_of_19-29,":  user.demographics.age["19-29"],
    "age_confidence_probability_of_30-39":  user.demographics.age["30-39"],
    "age_confidence_probability_of_>=40":  user.demographics.age[">=40"],
    "org_confidence_probability_of_non-org":  user.demographics.org["non-org"],
    "org_confidence_probability_of_is-org":  user.demographics.org["is-org"],
    // include the following fields if you want
    "created_at": user.created_at,
    "followers_count": user.followers_count,
    "friends_count": user.friends_count,
    "statuses_count": user.statuses_count,
    "favourites_count": user.favourites_count,
    "listed_count": user.listed_count,
    "verified": user.verified,
    "protected": user.protected,
    "geo_enabled": user.geo_enabled,
    "contributors_enabled": user.contributors_enabled,
  };
}

function feature_extract_tweets_list(tweetObjectsData: Array<TweetObject>) {
  return tweetObjectsData.map((tweet) => feature_extract_tweet(tweet));
}

function feature_extract_users_list(userObjectsData: Array<UserObject>) {
  return userObjectsData.map((user) => feature_extract_user(user));
}

function aggregate_tweets_list(tweetObjectsData: Array<TweetObject>) {
  let newTweetObjectsData = tweetObjectsData.map((tweet) => feature_extract_tweet(tweet));
  let aggregatedResult = {
    "sentiment_count": { 
      // count the number of tweets with sentiment "negative", "positive", "neutral"
      "negative": newTweetObjectsData.filter((tweet) => tweet.sentiment_prediction === "negative").length,
      "positive": newTweetObjectsData.filter((tweet) => tweet.sentiment_prediction === "positive").length, 
      "neutral": newTweetObjectsData.filter((tweet) => tweet.sentiment_prediction === "neutral").length, 
    },
  };
}

class Graph {
  adjacencyList: Map<string, Map<string, number>>;

  constructor() {
      this.adjacencyList = new Map();
  }

  addNode(keyword: string) {
      if (!this.adjacencyList.has(keyword)) {
          this.adjacencyList.set(keyword, new Map());
      }
  }

  addEdge(keyword1: string, keyword2: string) {
    if (!this.adjacencyList.has(keyword1)) {
        this.addNode(keyword1);
    }
    if (!this.adjacencyList.has(keyword2)) {
        this.addNode(keyword2);
    }

    const node1 = this.adjacencyList.get(keyword1);
    const node2 = this.adjacencyList.get(keyword2);

    if (node1 && node2) {
        // Ensure that node1 and node2 are not undefined
        if (node1.has(keyword2)) {
            node1.set(keyword2, node1.get(keyword2)! + 1); // Use ! to tell TypeScript it's not null or undefined
        } else {
            node1.set(keyword2, 1);
        }

        if (node2.has(keyword1)) {
            node2.set(keyword1, node2.get(keyword1)! + 1); // Use ! to tell TypeScript it's not null or undefined
        } else {
            node2.set(keyword1, 1);
        }
    }
}


  printGraph() {
      for (const [keyword, neighbors] of this.adjacencyList.entries()) {
          const neighborList = Array.from(neighbors.entries()).map(([neighbor, value]) => `${neighbor} (${value})`);
          console.log(`${keyword} -> ${neighborList.join(', ')}`);
      }
  }
}

function createGraph(lists: string[][]) {
  const graph = new Graph();

  for (const list of lists) {
      for (let i = 0; i < list.length; i++) {
          for (let j = i + 1; j < list.length; j++) {
              graph.addEdge(list[i], list[j]);
          }
      }
  }

  return graph;
}

// Example usage
const keywordLists = [["apple", "banana", "cherry"], ["banana", "date", "elderberry"], ["date", "fig"]];
const keywordGraph = createGraph(keywordLists);
keywordGraph.printGraph();


function aggregateTweetObjectsAnalysisResult(tweetObjectsList : Array<TweetObject>) {
  const sentimentCount = { negative: 0, positive: 0, neutral: 0 };
  const topicsCount = {};
  const keywordsCount = {};
  const keywordsPairs = {};

  for (const tweetObject of tweetObjectsList) {

    const textAnalyzedResult = tweetObject.text_analyzed;

    // Count topics
    const topic = textAnalyzedResult.topics;
    const highestScoreTopic = topic.reduce((prev, current) =>
      current[1] > prev[1] ? current : prev
    );
    topicsCount[highestScoreTopic[0]] = (topicsCount[highestScoreTopic[0]] || 0) + 1;

    // Count sentiment
    const sentimentResult = textAnalyzedResult.sentiment.result;
    sentimentCount[sentimentResult] =
      (sentimentCount[sentimentResult] || 0) + 1;

    const keywords = textAnalyzedResult.associated_keywords;

    // Keyword count
    for (const keyword of keywords) {
      keywordsCount[keyword] = (keywordsCount[keyword] || 0) + 1;
    }

    // Keyword pairs
    for (let i = 0; i < keywords.length; i++) {
      for (let j = i + 1; j < keywords.length; j++) {
        const smaller_keyword = keywords[i] < keywords[j] ? keywords[i] : keywords[j];
        const bigger_keyword = keywords[i] < keywords[j] ? keywords[j] : keywords[i];
        const keywordsPair = `${smaller_keyword},${bigger_keyword}`;
        keywordsPairs[keywordsPair] = (keywordsPairs[keywordsPair] || 0) + 1;
      }
    }
  }

  const keywordsPairsArray = Object.entries(keywordsPairs).map(([keywordsPair, count]) => {
    return { keywords: keywordsPair.split(','), count };
  });

  return [topicsCount, sentimentCount, keywordsCount, keywordsPairsArray];
}

function aggregateUserObjectsAnalysisResult(data : Array<UserObject>) {
  const countriesCount = {};
  const gendersCount = { female: 0, male: 0 };
  const ageGroupsCount = { "19-29": 0, "30-39": 0, "<=18": 0, ">=40": 0 };

  for (const userObject of data) {
    // Count country codes
    const countryCode = userObject.location_analyzed.country_code;
    countriesCount[countryCode] = (countriesCount[countryCode] || 0) + 1;

    // Count genders
    const genderScores = userObject.demographics.gender;
    const gender = Object.keys(genderScores).reduce((prev, current) =>
      genderScores[current] > genderScores[prev] ? current : prev
    );
    gendersCount[gender]++;

    // Count age
    const ageScores = userObject.demographics.age;
    const age = Object.keys(ageScores).reduce((prev, current) =>
      ageScores[current] > ageScores[prev] ? current : prev
    );
    ageGroupsCount[age]++;
  }

  return [countriesCount, gendersCount, ageGroupsCount];
}
