import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3'; // Import D3 library
import VisHeader from '../VisHeader';
import { Tooltip } from 'recharts';
import { ForceGraph2D } from 'react-force-graph';
import DATATYPES from '../../constants/dataTypes';

const data = DATATYPES.knowledgeGraph.data;

const KnowledgeGraph = () => {

  return (
    <div className="vis-container">
      <VisHeader title="Knowledge Graph" subtitle="Bar Subtitle" />
      <div className="vis-svg-container">
        <ForceGraph2D
          graphData={data}
          width={490}
          height={390}
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
