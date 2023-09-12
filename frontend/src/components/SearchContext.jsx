import { useEffect, createContext, useContext, useState } from "react";

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

  const updateRealData = (data) => {
    console.log("in SearchContext.jsx, before updateRealData:");
    console.log("realData value:");
    console.log(realData);
    console.log("data received:");
    console.log(data);
    setRealData(data);
    console.log("after setRealData:");
    console.log("realData value:");
    console.log(realData);
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
