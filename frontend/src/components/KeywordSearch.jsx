import search from "../assets/search.svg";
import { useState } from "react";
import light from "../assets/light.svg";
import dark from "../assets/dark.svg";
import { useActionData, useNavigate, Form } from "react-router-dom";

const KeywordSearch = () => {
  const [mode, setMode] = useState(true);

  const actionData = useActionData();

  function toggleTheme() {
    let element = document.body;
    element.classList.toggle("dark");
    mode ? setMode(false) : setMode(true);
  }

  return (
    <div className="keywordsearch-bar">
      <img className="sidebar-icon" src={search} alt="search" />
      <Form method="post" action="/search">
        <input
          className="keywordsearch-input"
          type="text"
          id="keyword"
          name="keyword"
          placeholder="Search Term"
        />
      </Form>
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

export const keywordAction = async ({ request }) => {
  const data = await request.formData();

  const submission = {
    keyword: data.get(keyword),
  };

  console.log(submission);
};
