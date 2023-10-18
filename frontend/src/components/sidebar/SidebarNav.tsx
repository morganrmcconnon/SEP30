import dashboard from "../../assets/dashboard.svg";
import contact from "../../assets/contact.svg";
// import file from "../../assets/file.svg";
import information from "../../assets/information.svg";

import { Link } from "react-router-dom";

const SidebarNav = () => {
  return (
    <>
      <h3 className="sidebar-title">MAIN MENU</h3>
      <nav>
        <ul className="sidebar-list">
          <Link to="/">
            <li>
              <img className="sidebar-icon" src={dashboard} alt="dashboard" />
              <h3>Dashboard</h3>
            </li>
          </Link>
          <Link to="/about">
            <li>
              <img className="sidebar-icon" src={information} alt="about" />
              <h3>About</h3>
            </li>
          </Link>
          <Link to="/contact">
            <li>
              <img className="sidebar-icon" src={contact} alt="contact" />
              <h3>Contact</h3>
            </li>
          </Link>
        </ul>
      </nav>
    </>
  );
};

export default SidebarNav;
