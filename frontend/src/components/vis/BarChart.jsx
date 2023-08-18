import React, { useEffect, useRef, useState } from "react";
import Plot from "react-plotly.js";
import arrowAll from "../../assets/arrow-all.svg";
import dotsVertical from "../../assets/dots-vertical.svg";

const BarChart = () => {

  const chartRef = useRef(null);

  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);
  const [layout, setLayout] = useState({});

  useEffect(() => {
    if (chartRef.current) {
      console.log(chartRef.current.parentElement.clientWidth);
      setWidth(chartRef.current.parentElement.clientWidth);
      setHeight(chartRef.current.parentElement.clientHeight);
      setLayout({
        // title: "Least Used Feature",
        plot_bgcolor: "#d0ebff",
        // paper_bgcolor: "#d3f9d8",
        // width: width,
        height: height,
        margin: {
          l: 100,
          r: 40,
          b: 40,
          t: 100,
          pad: 4
        },
      })
    }
  }, []);

  var trace1 = {
    y: ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"],
    x: [20, 14, 23, 25, 22],
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
    orientation: "h",
  };

  var data = [trace1];

  var config = { 
    responsive: true, 
    toggleSpikelines: true,
    // scrollZoom: true,
    // staticPlot: true, 
    editable: true,
    // toImageButtonOptions: {
    //   format: 'svg', // one of png, svg, jpeg, webp
    //   filename: 'custom_image',
    //   height: 500,
    //   width: 700,
    //   scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
    // }
  }

  return (
    <div className="vis-container" ref={chartRef}>
      <div className="vis-header" style={{
        position: 'absolute',
        zIndex: 1,
        pointerEvents: 'none'
      }}>
        <div className="vis-drag-handle" style={{ pointerEvents: 'auto', cursor: 'move' }}>
          <img src={arrowAll} />
        </div>
        <div className="vis-header-title" style={{ pointerEvents: 'auto' }}>
          <h3>Bar Chart</h3>
          <p className="text-subtitle">Subtitle</p>
        </div>
        <img className="vis-dots" src={dotsVertical} style={{ pointerEvents: 'none', cursor: 'grab' }} />
      </div>
      <Plot data={data} layout={layout} config={config} useResizeHandler={true}
        style={{ width: '100%', height: '100%' }} >
      </Plot>
    </div>
  );
};

export default BarChart;
