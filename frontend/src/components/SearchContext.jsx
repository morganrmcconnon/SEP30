import { useEffect, createContext, useContext, useState } from "react";
import ColorVar from "./ColorVar";

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

  const [demoGraphic1, setDemoGraphic1] = useState({
    title: 'Demographic 1',
    subTitle: 'Age',
    data: [
      { name: 'Under 18', percent: 25, color: ColorVar.blue },
      { name: '19 - 29', percent: 25, color: '#50cc65' },
      { name: '30 - 39', percent: 25, color: ColorVar.orange },
      { name: '40 and above', percent: 25, color: '#eeeeef' },
    ],
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

    let d1 = response_data[5]["<=18"];
    let d2 = response_data[5]["19-29"];
    let d3 = response_data[5]["30-39"];
    let d4 = response_data[5][">=40"];

    let p1 = d1 / (d1 + d2 + d3 + d4) * 100;
    let p2 = d2 / (d1 + d2 + d3 + d4) * 100;
    let p3 = d3 / (d1 + d2 + d3 + d4) * 100;
    let p4 = d4 / (d1 + d2 + d3 + d4) * 100;

    setDemoGraphic1({
      title: 'Demographic 1',
      subTitle: 'Age',
      data: [
        { name: 'Under 18', percent: p1, color: ColorVar.blue },
        { name: '19 - 29', percent: p2, color: '#50cc65' },
        { name: '30 - 39', percent: p3, color: ColorVar.orange },
        { name: '40 and above', percent: p4, color: '#eeeeef' },
      ],
    });

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
    <SearchContext.Provider value={{ search, updateSearch, realData, updateRealData, demoGraphic1 }}>
      {children}
    </SearchContext.Provider>
  );
};

export function useSearch() {
  return useContext(SearchContext);
}
