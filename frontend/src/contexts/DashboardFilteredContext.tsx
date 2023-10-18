import React, { createContext, useContext, useEffect, useState } from "react";

import { update_dashboard_data } from "../data/grids/functions/UpdateDashboardData";
// import { filter_data_by } from "../data/api/functions/FilterData";
import { aggregate_data } from "../data/api/functions/AggregateData";

import { DATATYPES } from "../data/grids/constants/DATATYPES";
import { GridsDataType } from "../data/grids/types/GridsDataType";
import { BackendOutput } from "../data/api/types/BackendOutput";
import { TweetObject } from "../data/api/types/TweetObject";
import { UserObject } from "../data/api/types/UserObject";

export type FilterOptionsType = {
  sentiment: string | null,
  topic: string | null,
  keyword: string | null,
  age: string | null,
  gender: string | null,
  location: string | null,
  date: string | null,
};

function filter_tweets_list_by(
  tweet_objects: Array<TweetObject>,
  filter_option: FilterOptionsType,
) {
  return tweet_objects.filter(tweet_object => {
    const sentiment_predicted = tweet_object.sentiment;
    const associated_keywords = tweet_object.text_processed;
    const original_text = tweet_object.text;
    const text_in_english = tweet_object.text_in_english;
    const user_object = tweet_object.user;
    const country_code = user_object.country_code;
    const age_predicted = user_object.age;
    const gender_predicted = user_object.gender;
    return (
      (filter_option.sentiment === null || sentiment_predicted === filter_option.sentiment)
      && (filter_option.topic === null || tweet_object.topic_lda.related_topics.cosine_similarity.includes(filter_option.topic))
      && (filter_option.keyword === null || associated_keywords.includes(filter_option.keyword) || original_text.includes(filter_option.keyword) || text_in_english.includes(filter_option.keyword))
      && (country_code === filter_option.location || filter_option.location === null)
      && (age_predicted === filter_option.age || filter_option.age === null)
      && (gender_predicted === filter_option.gender || filter_option.gender === null)
    );
  });
}

const defaultFilterOptions: FilterOptionsType = {
  sentiment: null,
  topic: null,
  keyword: null,
  gender: null,
  location: null,
  age: null,
  date: null,
};


// Define the type for the context
type DashboardFilteredContextType = {
  filterOptions: FilterOptionsType,
  updateFilterOption: (filter_option_name: keyof FilterOptionsType, filter_option_value: string | null) => void,
  tweetOjects: Array<TweetObject>,
  backendData?: BackendOutput,
  updateBackendData: (response_data: BackendOutput) => void,
  resetFilter: () => void,
  dashboardData: GridsDataType,
}

const DashboardFilteredContext = createContext<DashboardFilteredContextType>({
  filterOptions: defaultFilterOptions,
  updateFilterOption: () => { },
  resetFilter: () => { },
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
    // Use this code if you want to get data from the database
    // // Get last week's data

    // const lastMonday = new Date();
    // lastMonday.setDate(lastMonday.getDate() - ((lastMonday.getDay() + 6) % 7));
    // lastMonday.setHours(0, 0, 0, 0);

    // const lastLastMonday = new Date(lastMonday);
    // lastLastMonday.setDate(lastLastMonday.getDate() - 7);

    // // For testing purposes only
    // // Since we only have data for 2022 (from Internet Archive's Twitter Stream), we need to set the year to 2022 to get the data for the last week of 2022
    // lastLastMonday.setFullYear(2022);
    // lastLastMonday.setMonth(10);
    // lastLastMonday.setDate(1);
    
    // lastMonday.setFullYear(2022);
    // lastMonday.setMonth(10);
    // lastMonday.setDate(15);

    // const requestOptions = {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ 
    //     'start': lastLastMonday, 
    //     'end': lastMonday,
    //   }),
    // };
    // fetch("/api/data", requestOptions)
    fetch("/api/get_cached")
      .then((res) => res.json())
      .then((data) => {
        updateBackendData(data);
      })
      .catch((err) => {
        console.log(`Something went wrong with getting data from the backend.`);
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
    updateDashboardBy({ ...filterOptions, [filter_option_name]: filter_option_value });
  };

  const resetFilterOptions = () => {
    updateDashboardBy(defaultFilterOptions);
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


  const updateDashboardBy = (filter_option: FilterOptionsType) => {

    setFilterOptions(filter_option);
    const tweet_objects = backendData?.tweet_objects ?? [];
    const filtered_tweets_list = filter_tweets_list_by(tweet_objects, filter_option);
    const filtered_users_list = filtered_tweets_list.map((tweet) => { return tweet.user; });

    setTweetObjects(filtered_tweets_list);

    if (backendData !== undefined) {
      updateDashboardData(backendData, filtered_tweets_list, filtered_users_list);
    }
  };

  return (
    <DashboardFilteredContext.Provider value={{
      filterOptions: filterOptions,
      backendData: backendData,
      updateBackendData: updateBackendData,
      dashboardData: dashboardData,
      updateFilterOption: updateFilterOption,
      resetFilter: resetFilterOptions,
      tweetOjects: tweetObjects,
    }}>
      {children}
    </DashboardFilteredContext.Provider>
  );
};

export function useDashboardFilteredContext() {
  return useContext(DashboardFilteredContext);
}
