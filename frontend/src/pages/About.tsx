import "../styles/styles.css";

import AboutGrids from "../components/AboutGrids.tsx";
import KeywordSearch from "../components/KeywordSearch";
import Sidebar from "../components/Sidebar";
import { SearchProvider } from "../contexts/SearchContext";

export default function About() {
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
          <AboutGrids />
        </div>
      </div>
    </SearchProvider>
  );
}
