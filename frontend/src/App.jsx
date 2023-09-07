import { useState } from "react";
import "./styles/styles.css";
import Sidebar from "./components/Sidebar";
import KeywordSerch from "./components/KeywordSearch";
import DashboardVis from "./components/DashboardVis";
import Counter from "./components/Counter";
import { SearchProvider } from "./components/SearchContext";
import Search from "antd/es/input/Search";

function App() {
  return (
    <SearchProvider>
      <div className="body-container">
        <div className="sidebar-container">
          <Sidebar />
          <Counter />
        </div>
        <div className="keywordsearch-container">
          <KeywordSerch />
        </div>
        <div className="dashboard-container">
          <DashboardVis />
        </div>
      </div>
    </SearchProvider>
  );
}

export default App;
