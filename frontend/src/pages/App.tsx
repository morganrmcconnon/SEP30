import "../styles/styles.css";

import DashboardVis from "../components/DashboardVis.tsx";
import KeywordSearch from "../components/KeywordSearch.jsx";
import Sidebar from "../components/Sidebar.jsx";
import { SearchProvider } from "../contexts/SearchContext.jsx";

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
