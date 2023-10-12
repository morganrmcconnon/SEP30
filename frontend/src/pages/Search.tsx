import { useActionData } from "react-router-dom";

import "../styles/styles.css";

import Sidebar from "../components/Sidebar";
import KeywordSearch from "../components/KeywordSearch";
import { DashboardContextProvider } from "../contexts/DashboardContext";

function Search() {
  const keyword : any = useActionData();

  return (
    <DashboardContextProvider>
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
    </DashboardContextProvider>
  );
}

export default Search;
