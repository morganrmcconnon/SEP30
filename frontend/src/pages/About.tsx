import "../styles/styles.css";

// import file from "../../assets/file.svg";
import information from "../assets/information.svg";

import AboutGrids from "../components/main/AboutGrids.tsx";
import PageHeader from "../components/header/PageHeader.tsx";
import Sidebar from "../components/sidebar/Sidebar.tsx";

export default function About() {
  return (
    <div className="body-container">
      <div className="sidebar-container">
        <Sidebar />
      </div>
      <div className="keywordsearch-container">
        <PageHeader icon={information} title={"Data science methods used by the system"} />
      </div>
      <div className="dashboard-container">
        <AboutGrids />
      </div>
    </div>
  );
}
