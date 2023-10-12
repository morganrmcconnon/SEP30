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
  sentiment?: string | null,
  topic?: string | null,
  keyword?: string | null,
  age?: string | null,
  gender?: string | null,
  location?: string | null,
};

const defaultFilterOptions: FilterOptionsType = {
  sentiment: null,
  topic: null,
  keyword: null,
  gender: null,
  location: null,
  age: null,
};


// Define the type for the context
type DashboardFilteredContextType = {
  filterOptions: FilterOptionsType,
  updateFilterOptions: (filter_option_name: keyof FilterOptionsType, filter_option_value: string | null) => void,
  tweetOjects?: Array<TweetObject>,
  backendData?: BackendOutput,
  updateBackendData: (response_data: BackendOutput) => void,
  resetFilterOptions: () => void,
  dashboardData: GridsDataType,
}

const DashboardFilteredContext = createContext<DashboardFilteredContextType>({
  filterOptions: defaultFilterOptions,
  updateFilterOptions: () => { },
  resetFilterOptions: () => { },
  backendData: undefined,
  tweetOjects: [],
  updateBackendData: () => { },
  dashboardData: DATATYPES,
});

export const DashboardFilteredContextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {

  const [filterOptions, setFilterOptions] = useState<FilterOptionsType>(defaultFilterOptions);

  const [backendData, setBackendData] = useState<BackendOutput>();

  const [dashboardData, setDashboardData] = useState<GridsDataType>(DATATYPES);

  const [tweetObjects, setTweetObjects] = useState<Array<TweetObject>>([]);

  const updateBackendData = (response_data: BackendOutput) => {

    setBackendData(response_data);

    const tweet_objects = response_data.tweet_objects ?? [];
    const user_objects = tweet_objects.map((tweet) => { return tweet.user; });

    setTweetObjects(tweet_objects);

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
        console.log(`Something went wrong with executing endpoint "/backend/get_cached"`);
        console.log(err);
        console.error(err);
      });
  }, []);

  const updateFilterOption = (filter_option_name: keyof FilterOptionsType, filter_option_value: string | null) => {
    if (filter_option_value != undefined
      && filter_option_value != null
      && filter_option_value === filterOptions[filter_option_name]) {
      filter_option_value = null;
    }
    updateFilterOptions({ ...filterOptions, [filter_option_name]: filter_option_value });
  };

  const resetFilterOptions = () => {
    updateFilterOptions(defaultFilterOptions);
  }

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
    const week_line_graphs = aggregate_data_info.week;

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
      week_line_graphs,
    );

    setDashboardData(newDashboardData);
  };


  const updateFilterOptions = ({
    sentiment,
    topic,
    keyword,
    gender,
    location,
    age,
  } : FilterOptionsType
  ) => {

    setFilterOptions({
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
    const user_objects = tweet_objects.map((tweet) => { return tweet.user; });

    const filtered_data = filter_data_by(tweet_objects, user_objects, sentiment, topic, keyword, location, gender, age);
    const sub_list_of_tweets = filtered_data.new_tweet_objects;
    const sub_list_of_users = filtered_data.new_user_objects;

    setTweetObjects(sub_list_of_tweets);

    if (backendData !== undefined) {
      updateDashboardData(backendData, sub_list_of_tweets, sub_list_of_users);
    }
  };

  return (
    <DashboardFilteredContext.Provider value={{
      filterOptions: filterOptions,
      backendData: backendData,
      updateBackendData: updateBackendData,
      dashboardData: dashboardData,
      updateFilterOptions: updateFilterOption,
      resetFilterOptions: resetFilterOptions,
      tweetOjects: tweetObjects,
    }}>
      {children}
    </DashboardFilteredContext.Provider>
  );
};

export function useDashboardFilteredContext() {
  return useContext(DashboardFilteredContext);
}
