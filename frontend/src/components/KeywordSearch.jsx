import search from "../assets/search.svg";
import { useState } from "react";
import light from "../assets/light.svg";
import dark from "../assets/dark.svg";

const KeywordSearch = () => {
  const [mode, setMode] = useState(true);

  function toggleTheme() {
    let element = document.body;
    element.classList.toggle("dark");
    mode ? setMode(false) : setMode(true);
  }

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
      <div></div>
      <img
        className="toggle-mode"
        src={mode ? light : dark}
        onClick={toggleTheme}
      />
    </div>
  );
};

export default KeywordSearch;
