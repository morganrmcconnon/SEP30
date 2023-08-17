import arrowAll from "../../assets/arrow-all.svg";

const Map = () => {
  return (
    <div className="vis-container">
      <div className="vis-header">
        <div className="vis-drag-handle">
          <img src={arrowAll} />
          <div className="vis-header-title">
            <h3>Map</h3>
            <p className="text-subtitle">Location</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Map;
