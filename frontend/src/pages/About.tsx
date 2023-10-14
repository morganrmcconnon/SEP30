import "../styles/styles.css";

import AboutGrids from "../components/AboutGrids.tsx";
import KeywordSearch from "../components/KeywordSearch";
import Sidebar from "../components/sidebar/Sidebar.tsx";
import { DashboardFilteredContextProvider } from "../contexts/DashboardFilteredContext.tsx";

export default function About() {
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
          <AboutGrids />
        </div>
      </div>
    </DashboardFilteredContextProvider>
  );
}
