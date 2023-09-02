import { useState } from "react";
import "./styles/styles.css";
import Sidebar from "./components/Sidebar";
import KeywordSerch from "./components/KeywordSearch";
import DashboardVis from "./components/DashboardVis";
import Counter from "./components/Counter";

function App() {
  return (
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
  );
}

export default App;
