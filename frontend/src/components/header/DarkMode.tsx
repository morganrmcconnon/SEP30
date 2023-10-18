import { useState } from "react";

import light from "../../assets/light.svg";
import dark from "../../assets/dark.svg";

import "react-grid-layout/css/styles.css";
import "../../styles/override.css";



const PageHeader = () => {
  const [mode, setMode] = useState(true);

  // const actionData = useActionData();

  function toggleTheme() {
    const element = document.body;
    element.classList.toggle("dark");
    mode ? setMode(false) : setMode(true);
  }

  return (
    <img
      className="toggle-mode"
      src={mode ? light : dark}
      onClick={toggleTheme}
    />
  );
};

export default PageHeader;

