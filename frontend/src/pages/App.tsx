import "../styles/styles.css";

import DashboardVis from "../components/main/DashboardVis.tsx";
import KeywordSearch from "../components/header/KeywordSearch.js";
import Sidebar from "../components/sidebar/Sidebar.js";
import SidebarPreferences from "../components/sidebar/SidebarPreferences.tsx";
import { DashboardFilteredContextProvider } from "../contexts/DashboardFilteredContext";

function App() {
  return (
    <DashboardFilteredContextProvider>
      <div className="body-container">
        <div className="sidebar-container">
          <Sidebar />
          <SidebarPreferences />
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
