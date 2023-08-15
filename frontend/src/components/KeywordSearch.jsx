import search from "../assets/search.svg";
import useState from "react";

const KeywordSearch = () => {
  return (
    <div className="keywordsearch-bar">
      <img className="sidebar-icon" src={search} alt="search" />
      <form>
        <input
          className="keywordsearch-input"
          type="text"
          id="keyword"
          name="keyword"
          placeholder="Search Term"
        />
      </form>
    </div>
  );
};

export default KeywordSearch;
