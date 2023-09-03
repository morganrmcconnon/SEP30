import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3'; // Import D3 library
import VisHeader from '../VisHeader';
import { Tooltip } from 'recharts';
import { ForceGraph2D } from 'react-force-graph';

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
        { source: 'Node 3', target: 'Node 4', value: 30 },
        { source: 'Node 2', target: 'Node 5', value: 10 },
        { source: 'Node 2', target: 'Node 6', value: 50 },
        // Add more links
      ]
    ,
  }
}) => {

  return (
    <div className="vis-container">
      <VisHeader title="Knowledge Graph" subtitle="Bar Subtitle" />
      <div className="vis-svg-container">
        <ForceGraph2D
          graphData={data}
          width={svgRef.current ? svgRef.current.clientWidth : 490}
          height={svgRef.current ? svgRef.current.clientHeight : 390}
          onNodeClick={(node) => console.log('Clicked:', node)}
          nodeAutoColorBy="group"
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.id;
            const fontSize = 12 / globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

            ctx.fillStyle = 'rgba(255, 255, 255, 1)';
            ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = node.color;
            ctx.fillText(label, node.x, node.y);

            node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
          }}
          nodePointerAreaPaint={(node, color, ctx) => {
            ctx.fillStyle = color;
            const bckgDimensions = node.__bckgDimensions;
            bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
          }}
          linkWidth={link => Math.sqrt(link.value)}
        />
      </div>
    </div>
  );
};

export default KnowledgeGraph;
