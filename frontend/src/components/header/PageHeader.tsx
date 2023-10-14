// import { useState } from "react";

// import light from "../../assets/light.svg";
// import dark from "../../assets/dark.svg";

import "react-grid-layout/css/styles.css";
import "../../styles/override.css";

type GreetingProps = {
  icon: string;
  title: string;
};

const PageHeader  : React.FC<GreetingProps> = (props) => {
  // const [mode, setMode] = useState(true);

  // const actionData = useActionData();

  // function toggleTheme() {
  //   let element = document.body;
  //   element.classList.toggle("dark");
  //   mode ? setMode(false) : setMode(true);
  // }

  return (
    <div className="keywordsearch-bar">
      <img className="sidebar-icon" src={props.icon} alt="search" />
      <h2>{props.title}</h2>
      {/*<img
        className="toggle-mode"
        src={mode ? light : dark}
        onClick={toggleTheme}
  />*/}
    </div>
  );
};

export default PageHeader;

