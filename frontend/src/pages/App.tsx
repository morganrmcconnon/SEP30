import "../styles/styles.css";

import DashboardVis from "../components/DashboardVis.tsx";
import KeywordSearch from "../components/KeywordSearch.jsx";
import Sidebar from "../components/Sidebar.jsx";
import { DashboardContextProvider } from "../contexts/DashboardContext.js";

function App() {
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
          <DashboardVis />
        </div>
      </div>
    </DashboardContextProvider>
  );
}

export default App;
