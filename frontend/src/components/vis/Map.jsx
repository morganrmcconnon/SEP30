import arrowAll from "../../assets/arrow-all.svg";
import dotsVertical from "../../assets/dots-vertical.svg";

import * as d3 from "d3";

const Map = () => {
  return (
    <div className="vis-container">
      <div className="vis-header">
        <div className="vis-drag-handle">
          <img src={arrowAll} />
        </div>
        <div className="vis-header-title">
          <h3>Map</h3>
          <p className="text-subtitle">Subtitle</p>
        </div>
        <img className="vis-dots" src={dotsVertical} />
      </div>
    </div>
  );
};

export default Map;
