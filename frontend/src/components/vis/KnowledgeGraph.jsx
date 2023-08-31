import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3'; // Import D3 library
import VisHeader from '../VisHeader';
import { Tooltip } from 'recharts';


const numNodes = 100; // Number of nodes
const numLinks = 150; // Number of links

const nodes = d3.range(numNodes).map(i => ({ id: `Node ${i}`, group: i % 10 + 1 }));
const links = d3.range(numLinks).map(i => ({ source: i % numNodes, target: (i + 10) % numNodes, value: 10 }));
console.log(nodes);
console.log(links);


const KnowledgeGraph = ({
  data = {
    nodes: [
      { id: 'Node 1', group: 1 },
      { id: 'Node 2', group: 1 },
      { id: 'Node 3', group: 2 },
      { id: 'Node 4', group: 2 },
      { id: 'Node 5', group: 2 },
      { id: 'Node 6', group: 2 },
      { id: 'Node 7', group: 2 },
      { id: 'Node 8', group: 2 },
      // Add more nodes
    ]
    ,
    links:
      [
        { source: 'Node 1', target: 'Node 2', value: 10 },
        { source: 'Node 1', target: 'Node 3', value: 20 },
        // Add more links
      ]
    ,
  }
}) => {


  const svgRef = useRef(null);
  const simulationRef = useRef(null);

  useEffect(() => {
    const width = 300;
    const height = 200;
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const links = data.links.map(d => ({ ...d }));
    const nodes = data.nodes.map(d => ({ ...d }));

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("x", d3.forceX())
      .force("y", d3.forceY());

    simulationRef.current = simulation;

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("style", "max-width: 100%; height: auto;")
      .call(d3.zoom().on("zoom", handleZoom));

    const container = svg.append("g");

    const link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", d => Math.sqrt(d.value));

    const node = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 5)
      .attr("fill", d => color(d.group))
      .on("mouseover", handleMouseOver)
      .on("mouseout", handleMouseOut)
      .on("click", handleNodeClick);

    node.append("title")
      .text(d => d.id);

    node.call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });

    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    function handleMouseOver(event, d) {
      d3.select(this)
        .attr("r", 10);

      const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("pointer-events", "none")
        .style("background-color", "white")
        .style("border", "1px solid #999")
        .style("padding", "5px")
        .style("opacity", 0.9)
        .style("font-size", "12px");

      tooltip.html(`${d.id}<br>Group: ${d.group}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");
    }

    function handleMouseOut() {
      d3.select(this)
        .attr("r", 5); // Reset node size on mouse out

      d3.select(".tooltip").remove();
    }

    function handleNodeClick(event, d) {
      const [x, y] = [d.x, d.y];
      const k = 2;

      svg.transition()
        .duration(750)
        .call(
          zoomRef.current.transform,
          d3.zoomIdentity
            .translate(width / 2, height / 2)
            .scale(k)
            .translate(-x, -y)
        );
    }

    function handleZoom(event) {
      container.attr("transform", event.transform);
    }

    return () => {
      simulation.stop();
    };
  }, [data]);

  return (
    <div className="vis-container">
      <VisHeader title="Knowledge Graph" subtitle="Bar Subtitle" />
      <div className="vis-svg-container">
        <svg ref={svgRef} />
      </div>
    </div>
  );
};

export default KnowledgeGraph;
