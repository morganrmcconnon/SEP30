import React, { useEffect } from "react";
import Plot from "react-plotly.js";

const BarChart = () => {
  var trace1 = {
    x: ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"],
    y: [20, 14, 23, 25, 22],
    marker: {
      color: [
        "rgba(204,204,204,1)",
        "rgba(222,45,38,0.8)",
        "rgba(204,204,204,1)",
        "rgba(204,204,204,1)",
        "rgba(204,204,204,1)",
      ],
    },
    type: "bar",
  };

  var data = [trace1];

  var layout = {
    // title: "Least Used Feature",
    plot_bgcolor: "#d0ebff",
    paper_bgcolor: "#d3f9d8",
    width: 395,
    height: 200,
    margin: {
      l: 30,
      r: 30,
      b: 30,
      t: 30,
      pad: 4
    },
  };

  return (
    <div className="vis-container">
      {" "}
      <div className="vis-header">
        <div className="vis-drag-handle">X</div>
      </div>
      <Plot data={data} layout={layout} />
    </div>
  );
};

export default BarChart;
