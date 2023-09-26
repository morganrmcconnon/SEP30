import React, { createContext, useContext, useEffect, useState } from "react";

import { update_dashboard_data } from "../data/grids/functions/FormatData";
import { filter_data_by } from "../data/api/functions/FilterData";
import { aggregate_data } from "../data/api/functions/AggregateData";

import { DATATYPES } from "../data/grids/constants/DATATYPES";
import { GridsDataType } from "../data/grids/types/GridsDataType";
import { BackendOutput } from "../data/api/types/BackendOutput";
import { TweetObject } from "../data/api/types/TweetObject";
import { UserObject } from "../data/api/types/UserObject";

type FilterOptionsType = {
  sentiment?: string | false,
  topic?: string | false,
  keyword?: string | false,
  age?: string | false,
  gender?: string | false,
  location?: string | false,
};

const defaultSearch: FilterOptionsType = {
  sentiment: false,
  topic: false,
  keyword: false,
  gender: false,
  location: false,
  age: false,
};


// Define the type for the context
type SearchContextType = {
  search: FilterOptionsType,
  updateFilterOption: (filter_option_name: keyof FilterOptionsType, filter_option_value: string | false) => void,
  backendData?: BackendOutput,
  updateBackendData: (response_data: BackendOutput) => void,
  dashboardData: GridsDataType,
}

const SearchContext = createContext<SearchContextType>({
  search: defaultSearch,
  updateFilterOption: () => { },
  backendData: undefined,
  updateBackendData: () => { },
  dashboardData: DATATYPES,
});

export const SearchProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {

  const [search, setSearch] = useState<FilterOptionsType>(defaultSearch);

  const [backendData, setBackendData] = useState<BackendOutput>();

  const [dashboardData, setDashboardData] = useState<GridsDataType>(DATATYPES);

  const updateBackendData = (response_data: BackendOutput) => {

    setBackendData(response_data);

    const tweet_objects = response_data.tweet_objects ?? [];
    const user_objects =  tweet_objects.map((tweet) => { return tweet.user; });

    updateDashboardData(response_data, tweet_objects, user_objects);
  };

  useEffect(() => {
    // Query the backend for the data on the first render
    fetch("/backend/get_cached")
      .then((res) => res.json())
      .then((data) => {
        updateBackendData(data);
      })
      .catch((err) => {
        console.log(`Something went wrong with executing endpoint "/backend/get_cached_static"`);
        console.log(err);
        console.error(err);
      });
  }, []);

  const updateFilterOption = (filter_option_name: keyof FilterOptionsType, filter_option_value: string | false) => {
    if (filter_option_value != false
      && filter_option_value != undefined
      && filter_option_value != null
      && filter_option_value === search[filter_option_name]) {
      filter_option_value = false;
    }
    updateSearch({ ...search, [filter_option_name]: filter_option_value });
  };

  const updateDashboardData = (backend_data: BackendOutput, tweet_objects: Array<TweetObject>, user_objects: Array<UserObject>) => {

    const aggregate_data_info = aggregate_data(tweet_objects, user_objects);
    const sentiment_count = aggregate_data_info.sentiment_count;
    const topic_count = aggregate_data_info.topic_count;
    const keyword_count = aggregate_data_info.keyword_count;
    const keyword_pairs_count = aggregate_data_info.keywordsPairsArray;
    const genders_count = aggregate_data_info.genders_count;
    const countries_count = aggregate_data_info.countries_count;
    const age_groups_count = aggregate_data_info.age_groups_count;
    const female_sentiment = aggregate_data_info.female_sentiment;
    const male_sentiment = aggregate_data_info.male_sentiment;

    const total_tweets_count = backend_data.aggregate_results.total_tweets_count ?? 0;
    const mental_health_related_tweets_count = backend_data.aggregate_results.related_tweets_count ?? 0;
    const tweets_displayed_count = tweet_objects.length;


    const newDashboardData = update_dashboard_data(
      total_tweets_count,
      mental_health_related_tweets_count,
      tweets_displayed_count,
      sentiment_count,
      topic_count,
      keyword_count,
      keyword_pairs_count,
      countries_count,
      age_groups_count,
      genders_count,
      female_sentiment,
      male_sentiment,
    );

    setDashboardData(newDashboardData);
  };


  const updateSearch = ({
    sentiment,
    topic,
    keyword,
    gender,
    location,
    age,
  }
    : {
      sentiment?: string | false,
      topic?: string | false,
      keyword?: string | false,
      gender?: string | false,
      location?: string | false,
      age?: string | false,
    }
  ) => {

    setSearch({
      sentiment: sentiment,
      topic: topic,
      keyword: keyword,
      gender: gender,
      location: location,
      age: age,
    });

    const topic_id = typeof topic === 'string' ? topic : '0';

    if (backendData?.lda_topic_model.keywords_representation[topic_id] !== undefined) {
      console.log("in SearchContext.jsx, updateSearch:");
      dashboardData.keywordsDistribution.data = backendData?.lda_topic_model.keywords_representation[topic_id].slice(0, 10).map((item) => { return { name: item[0], value: item[1] } });
    }

    const tweet_objects = backendData?.tweet_objects ?? [];
    const user_objects =  tweet_objects.map((tweet) => { return tweet.user; });

    const filtered_data = filter_data_by(tweet_objects, user_objects, sentiment, topic, keyword, location, gender, age);
    const sub_list_of_tweets = filtered_data.new_tweet_objects;
    const sub_list_of_users = filtered_data.new_user_objects;

    if (backendData !== undefined) {
      updateDashboardData(backendData, sub_list_of_tweets, sub_list_of_users);
    }
  };

  return (
    <SearchContext.Provider value={{ search: search, backendData: backendData, updateBackendData: updateBackendData, dashboardData, updateFilterOption: updateFilterOption }}>
      {children}
    </SearchContext.Provider>
  );
};

export function useSearchContext() {
  return useContext(SearchContext);
}
