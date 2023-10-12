import "../styles/styles.css";

import DashboardVis from "../components/DashboardVis.tsx";
import KeywordSearch from "../components/KeywordSearch.jsx";
import Sidebar from "../components/Sidebar.jsx";
import { DashboardFilteredContextProvider } from "../contexts/DashboardFilteredContext";

function App() {
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
          <DashboardVis />
        </div>
      </div>
    </DashboardFilteredContextProvider>
  );
}

export default App;
