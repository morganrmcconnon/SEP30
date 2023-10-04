import "../styles/styles.css";

import KeywordSearch from "../components/KeywordSearch";
import Sidebar from "../components/Sidebar";
import { SearchProvider } from "../contexts/SearchContext";

export default function About() {
  return (
    <SearchProvider>
      <div className="body-container">
        <div className="sidebar-container">
          <Sidebar />
        </div>
        <div className="keywordsearch-container">
          <KeywordSearch />
        </div>
        <div className="contact-div">
            <div>
                <h2>We'd Love to Hear From You</h2>
            </div>
            <div>
                <p>For any enquiries or suggestions please reach out via our <a href={'mailto:twittermentalhealth30@gmail.com'}>email</a></p>
            </div>
          </div>
      </div>
    </SearchProvider>
  );
}
