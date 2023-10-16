import "../styles/styles.css";

import contact from "../assets/contact.svg";

import PageHeader from "../components/header/PageHeader";
import Sidebar from "../components/sidebar/Sidebar";
import { DashboardFilteredContextProvider } from "../contexts/DashboardFilteredContext";

export default function About() {
  return (
    <DashboardFilteredContextProvider>
      <div className="body-container">
        <div className="sidebar-container">
          <Sidebar />
        </div>
        <div className="keywordsearch-container">
          <PageHeader icon={contact} title={"Contact us!"} />
        </div>
        <div className="contact-div">
          <div>
            <h2>We'd Love to Hear From You</h2>
          </div>
          <div>
            <p className="text-black-white">For any enquiries or suggestions please reach out via our <a href={'mailto:twittermentalhealth30@gmail.com'}>email</a></p>
          </div>
        </div>
      </div>
    </DashboardFilteredContextProvider>
  );
}
