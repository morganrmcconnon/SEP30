import search from "../assets/search.svg";

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
          placeholder="Search Data"
        ></input>
      </form>
    </div>
  );
};

export default KeywordSearch;
