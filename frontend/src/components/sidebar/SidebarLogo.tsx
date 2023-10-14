import logo from "../../assets/logo.png";

import { Link } from "react-router-dom";

const SidebarLogo = () => {
  return (
    <>
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
    </>
  );
};

export default SidebarLogo;
