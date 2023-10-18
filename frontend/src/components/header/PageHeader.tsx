import "react-grid-layout/css/styles.css";
import "../../styles/override.css";

import DarkMode from "./DarkMode";

const PageHeader  : React.FC<{
  icon: string;
  title: string;
}> = (props) => {

  return (
    <div className="keywordsearch-bar">
      <img className="sidebar-icon" src={props.icon} alt="search" />
      <h2>{props.title}</h2>
      <DarkMode />
    </div>
  );
};

export default PageHeader;

