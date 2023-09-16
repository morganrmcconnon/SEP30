import { useEffect, createContext, useContext, useState } from "react";

import display_backend_data_into_charts from "../constants/FormatData";
import DATATYPES from "../constants/dataTypes";

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
    
    const topic_number = isNaN(topic) ? 0 : parseInt(topic);

    if(realData !== undefined && realData["topics_values"] !== undefined && realData["topics_values"][topic_number] !== undefined) {
      console.log("in SearchContext.jsx, updateSearch:");
      dashboardData.keywordsDistribution.data = realData["topics_values"][topic_number].map((item) => { return { name: item[0], value: item[1] } });
    }

    setDashboardData(dashboardData);

    setSearch({
      sentiment: sentiment,
      topic: topic,
      keyword: keyword,
      gender: gender,
      location: location,
      age: age,
    });

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
