import React, { useEffect, useState, useRef } from 'react';
import { ForceGraph2D } from 'react-force-graph';

import VisHeader from '../grid_components/VisHeader';
import { useSearchContext } from '../../contexts/SearchContext';
import DATATYPES from '../../constants/dataTypes';

const KnowledgeGraph = () => {
  const { search, updateSearch, dashboardData } = useSearchContext();
  const data = dashboardData.knowledgeGraph;

  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className="vis-svg-container">
        <ForceGraph2D
          graphData={data.data}
          width={390}
          height={390}
          onNodeClick={(node) => console.log('Clicked:', node)}
          nodeAutoColorBy="group"
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.id;
            const fontSize = 2 * node.value / globalScale;
            console.log(fontSize);
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
          nodeRelSize={node => node.value}
          nodePointerAreaPaint={(node, color, ctx) => {
            ctx.fillStyle = color;
            const bckgDimensions = node.__bckgDimensions;
            bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
          }}
          linkWidth={
            link => {
              const averageLinkValue = data.data.links.reduce((acc, cur) => acc + cur.value, 0) / data.data.links.length;
              return (link.value / averageLinkValue) * 4;
            }
          }
        />
      </div>
    </div>
  );
};

export default KnowledgeGraph;
