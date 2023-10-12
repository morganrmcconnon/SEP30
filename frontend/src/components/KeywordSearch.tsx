import { useState } from "react";
import { /* useActionData, */ Form } from "react-router-dom";

import search from "../assets/search.svg";
import light from "../assets/light.svg";
import dark from "../assets/dark.svg";

import "react-grid-layout/css/styles.css";
import "../styles/override.css";

import { useSearchContext } from "../contexts/DashboardContext";

const KeywordSearch = () => {
  const [mode, setMode] = useState(true);
  const { updateFilterOptions: updateFilterOption } = useSearchContext();

  // const actionData = useActionData();

  function toggleTheme() {
    let element = document.body;
    element.classList.toggle("dark");
    mode ? setMode(false) : setMode(true);
  }

  function updateKeyword(e: any) {
    e.preventDefault();
    console.log(e)
    const str = e.target[0].value;
    console.log(str);
    if(str === "" || str === undefined || str === null) {
      updateFilterOption("keyword", false);
    }
    else {
      updateFilterOption("keyword", str);
    }
  }

  return (
    <div className="keywordsearch-bar">
      <img className="sidebar-icon" src={search} alt="search" />
      {/* <Form method="post" action="/search"> */}
      <Form onSubmit={updateKeyword}>
        <input
          className="keywordsearch-input"
          type="text"
          id="keyword"
          name="keyword"
          placeholder="Search Term or Keyword"
        />
      </Form>
      {/*<img
        className="toggle-mode"
        src={mode ? light : dark}
        onClick={toggleTheme}
  />*/}
    </div>
  );
};

export default KeywordSearch;

export const keywordAction = async ({ request }: { request: any }) => {
  const data = await request.formData();

  const submission = {
    keyword: data.get('keyword'),
  };

  console.log(submission);
};
