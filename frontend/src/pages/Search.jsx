import { useState } from "react";
import "../styles/styles.css";
import Sidebar from "../components/Sidebar";
import KeywordSerch from "../components/KeywordSearch";
import { useActionData } from "react-router-dom";

function Search() {
  const keyword = useActionData();

  return (
    <div className="body-container">
      <div className="sidebar-container">
        <Sidebar />
      </div>
      <div className="keywordsearch-container">
        <KeywordSerch />
      </div>
      <div className="dashboard-container">
        <h2>Keyword: {keyword}</h2>
      </div>
    </div>
  );
}

export default Search;
