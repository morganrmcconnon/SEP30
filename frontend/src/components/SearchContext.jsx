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
    <SearchContext.Provider value={{ search, updateSearch }}>
      {children}
    </SearchContext.Provider>
  );
};

export function useSearch() {
  return useContext(SearchContext);
}
