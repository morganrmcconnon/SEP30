import arrowAll from "../../assets/arrow-all.svg";

const Map = () => {
  return (
    <div className="vis-container">
      <div className="vis-header">
        <div className="vis-drag-handle">
          <img src={arrowAll} />
        </div>
      </div>
      Map
    </div>
  );
};

export default Map;
