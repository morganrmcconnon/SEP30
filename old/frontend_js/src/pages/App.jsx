import "../styles/styles.css";

import DashboardVis from "../components/DashboardVis";
import KeywordSearch from "../components/KeywordSearch";
import Sidebar from "../components/Sidebar";
import { SearchProvider } from "../contexts/SearchContext";

function App() {
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
          <DashboardVis />
        </div>
      </div>
    </SearchProvider>
  );
}

export default App;
