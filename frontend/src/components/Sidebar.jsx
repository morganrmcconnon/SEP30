import dashboard from "../assets/dashboard.svg";
import contact from "../assets/contact.svg";
import file from "../assets/file.svg";
import information from "../assets/information.svg";
import settings from "../assets/settings.svg";
import logo from "../assets/logo.png";

const Sidebar = () => {
  return (
    <div>
      <div className="sidebar-logo">
        <div>
          <img className="sidebar-logo-image" src={logo} alt="logo" />
        </div>
        <div>
          <h1>SEP30</h1>
          <p className="text-data">Mental Health Dashboard</p>
        </div>
      </div>
      <h3 className="sidebar-title">MAIN MENU</h3>
      <ul className="sidebar-list">
        <li>
          <img className="sidebar-icon" src={dashboard} alt="overview" />
          Overview
        </li>
        <li>
          <img className="sidebar-icon" src={file} alt="dashboard" />
          Dashboard
        </li>
        <li>
          <img className="sidebar-icon" src={contact} alt="contact" />
          Contact
        </li>
        <li>
          <img className="sidebar-icon" src={information} alt="about" />
          About us
        </li>
      </ul>
      <h3 className="sidebar-title">PREFERENCES</h3>
      <ul className="sidebar-list">
        <li>
          <img className="sidebar-icon" src={settings} alt="settings" />
          Settings
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
