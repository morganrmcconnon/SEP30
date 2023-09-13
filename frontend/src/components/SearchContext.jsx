import { useEffect, createContext, useContext, useState } from "react";
import display_backend_data_into_charts from "./FormatData";

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

    display_backend_data_into_charts(response_data);

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
  };

  return (
    <SearchContext.Provider value={{ search, updateSearch, realData, updateRealData }}>
      {children}
    </SearchContext.Provider>
  );
};

export function useSearch() {
  return useContext(SearchContext);
}
