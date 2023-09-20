import { useEffect, createContext, useContext, useState } from "react";

import { display_backend_data_into_charts, update_dashboard_data } from "../constants/FormatData";
import { filter_data_by } from "../constants/FilterData";
import { aggregate_data, aggregate_tweet_objects_list, aggregate_user_objects_list } from "../constants/AggregateData";

const SearchContext = createContext();

export const SearchProvider = ({ children }) => {
  const [search, setSearch] = useState({
    sentiment: false,
    topic: false,
    keyword: false,
    gender: false,
    location: false,
    age: false,
  });

  const [realData, setRealData] = useState({});
  
  const [dashboardData, setDashboardData] = useState(DATATYPES);

  const updateRealData = (response_data) => {
    console.log("in SearchContext.jsx, before updateRealData:");
    console.log("realData value:");
    console.log(realData);
    console.log("data received:");
    console.log(response_data);

    setRealData(response_data);

    console.log("after setRealData:");
    console.log("realData value:");
    console.log(realData);

    setDashboardData(display_backend_data_into_charts(response_data));

  };
  

  const updateSearch = ({
    sentiment,
    topic,
    keyword,
    gender,
    location,
    age,
  }) => {
    
    setSearch({
      sentiment: sentiment,
      topic: topic,
      keyword: keyword,
      gender: gender,
      location: location,
      age: age,
    });

    const topic_number = isNaN(topic) ? 0 : parseInt(topic);

    if(realData !== undefined && realData["topics_values"] !== undefined && realData["topics_values"][topic_number] !== undefined) {
      console.log("in SearchContext.jsx, updateSearch:");
      dashboardData.keywordsDistribution.data = realData["topics_values"][topic_number].map((item) => { return { name: item[0], value: item[1] } });
    }

    const tweet_objects = realData["tweet_objects"];
    const user_objects = realData["user_objects"];

    const filtered_data = filter_data_by(tweet_objects, user_objects, sentiment, topic, keyword, location, gender, age);
    const sub_list_of_tweets = filtered_data.new_tweet_objects;
    const sub_list_of_users = filtered_data.new_user_objects;
    
    const aggregate_data_info = aggregate_data(sub_list_of_tweets, sub_list_of_users);
    const sentiment_count = aggregate_data_info.sentiment_count;
    const topic_count = aggregate_data_info.topic_count;
    const keyword_count = aggregate_data_info.keyword_count;
    const keyword_pairs_count = aggregate_data_info.keywordsPairsArray;
    const genders_count = aggregate_data_info.genders_count;
    const countries_count = aggregate_data_info.countries_count;
    const age_groups_count = aggregate_data_info.age_groups_count;
    const orgs_count = aggregate_data_info.org_count;

    const tweets_amount_info = realData["tweets_amount_info"];
   
    const total_tweets_count = tweets_amount_info['total_tweets_count'];
    const mental_health_related_tweets_count = tweets_amount_info['mental_health_related_tweets_count'];
    const tweets_displayed_count = sub_list_of_tweets.length;

    const newDashboardData = update_dashboard_data(total_tweets_count, mental_health_related_tweets_count, tweets_displayed_count, sentiment_count, topic_count, keyword_count, keyword_pairs_count, genders_count, countries_count, age_groups_count);

    setDashboardData(newDashboardData);

  };

  return (
    <SearchContext.Provider value={{ search, updateSearch, realData, updateRealData, dashboardData }}>
      {children}
    </SearchContext.Provider>
  );
};

export function useSearchContext() {
  return useContext(SearchContext);
}
