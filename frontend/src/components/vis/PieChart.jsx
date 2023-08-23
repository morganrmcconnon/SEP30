import * as d3 from "d3";
import { useState, useRef, useEffect } from "react";
import arrowAll from "../../assets/arrow-all.svg";
import dotsVertical from "../../assets/dots-vertical.svg";

const PieChart = () => {
  const svgRef = useRef();

  useEffect(() => {
    const width = 350,
      height = 350,
      margin = 40;

    const svg = d3
      .select(svgRef.current)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    const radius = Math.min(width, height) / 2 - margin;

    // Create dummy data
    const data = { a: 9, b: 20, c: 30, d: 8 };

    // set the color scale
    const color = d3
      .scaleOrdinal()
      .range(["#51CF66", "#339AF0", "#FF922B", "#FFFFFF"]);

    // Compute the position of each group on the pie:
    const pie = d3.pie().value(function (d) {
      return d[1];
    });
    const data_ready = pie(Object.entries(data));

    // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
    svg
      .selectAll("whatever")
      .data(data_ready)
      .join("path")
      .attr("d", d3.arc().innerRadius(0).outerRadius(radius))
      .attr("fill", function (d) {
        return color(d.data[1]);
      })
      .attr("stroke", "black")
      .style("stroke-width", "2px")
      .style("opacity", 0.7);
  });

  return (
    <div className="vis-container">
      <div className="vis-header">
        <div className="vis-drag-handle">
          <img src={arrowAll} />
        </div>
        <div className="vis-header-title">
          <h3>PieChart</h3>
          <p className="text-subtitle">Subtitle</p>
        </div>
        <img className="vis-dots" src={dotsVertical} />
      </div>
      <div>
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
};

export default PieChart;
