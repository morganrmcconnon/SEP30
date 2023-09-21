import { useActionData } from "react-router-dom";

import "../styles/styles.css";

import Sidebar from "../components/Sidebar";
import KeywordSearch from "../components/KeywordSearch";
import { SearchProvider } from "../contexts/SearchContext";

function Search() {
  const keyword : any = useActionData();

  return (
    <SearchProvider>
      <div className="body-container">
        <div className="sidebar-container">
          <Sidebar />
        </div>
        <div className="keywordsearch-container">
          <KeywordSearch />
        </div>
        <div className="dashboard-container">
          <h2>Keyword: {keyword}</h2>
        </div>
      </div>
    </SearchProvider>
  );
}

export default Search;
