import { useActionData } from "react-router-dom";

import "../styles/styles.css";

import Sidebar from "../components/sidebar/Sidebar";
import KeywordSearch from "../components/KeywordSearch";
import { DashboardFilteredContextProvider } from "../contexts/DashboardFilteredContext";

function Search() {
  const keyword : any = useActionData();

  return (
    <DashboardFilteredContextProvider>
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
    </DashboardFilteredContextProvider>
  );
}

export default Search;
