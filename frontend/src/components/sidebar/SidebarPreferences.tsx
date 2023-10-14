// import file from "../../assets/file.svg";
import settings from "../../assets/settings.svg";
import reset from "../../assets/reset.svg"

import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";

const SidebarPreferences = () => {
  const { resetFilter } = useDashboardFilteredContext();
  return (
    <>
      <h3 className="sidebar-title">PREFERENCES</h3>
      <nav>
        <ul className="sidebar-list">
          <li>
            <img className="sidebar-icon" src={settings} alt="settings" />
            <h3>Settings</h3>
          </li>
          <li onClick={() => resetFilter()}>
            <img className="sidebar-icon" src={reset} alt="reset" />
            <h3>Reset Filters</h3>
          </li>
        </ul>
      </nav>
    </>
  );
};

export default SidebarPreferences;
