import dashboard from "../assets/dashboard.svg";
import contact from "../assets/contact.svg";
import file from "../assets/file.svg";
import information from "../assets/information.svg";
import settings from "../assets/settings.svg";
import logo from "../assets/logo.png";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div>
      <Link to="/">
        <div className="sidebar-logo">
          <div>
            <img className="sidebar-logo-image" src={logo} alt="logo" />
          </div>
          <div>
            <h1>SEP30</h1>
            <p className="text-data">Mental Health Dashboard</p>
          </div>
        </div>
      </Link>
      <h3 className="sidebar-title">MAIN MENU</h3>
      <nav>
        <ul className="sidebar-list">
          <li>
            <img className="sidebar-icon" src={dashboard} alt="overview" />
            <h3>Overview</h3>
          </li>
          <li>
            <img className="sidebar-icon" src={file} alt="dashboard" />
            <h3>Dashboard</h3>
          </li>
          <li>
            <img className="sidebar-icon" src={contact} alt="contact" />
            <h3>Contact</h3>
          </li>
          <li>
            <img className="sidebar-icon" src={information} alt="about" />
            <h3>About us</h3>
          </li>
        </ul>
      </nav>
      <h3 className="sidebar-title">PREFERENCES</h3>
      <nav>
        <ul className="sidebar-list">
          <li>
            <img className="sidebar-icon" src={settings} alt="settings" />
            <h3>Settings</h3>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
