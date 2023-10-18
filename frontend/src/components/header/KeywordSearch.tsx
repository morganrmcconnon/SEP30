import { /* useActionData, */ Form } from "react-router-dom";

import search from "../../assets/search.svg";

import "react-grid-layout/css/styles.css";
import "../../styles/override.css";

import DarkMode from "./DarkMode";

import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";

const KeywordSearch = () => {
  const { updateFilterOption: updateFilterOption } = useDashboardFilteredContext();

  // const actionData = useActionData();

  function updateKeyword(e: any) {
    e.preventDefault();
    console.log(e)
    const str = e.target[0].value;
    console.log(str);
    if (str === "" || str === undefined || str === null) {
      updateFilterOption("keyword", null);
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
      <DarkMode />
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
