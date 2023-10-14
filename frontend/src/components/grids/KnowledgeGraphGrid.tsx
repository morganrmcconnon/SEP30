import { ForceGraph2D } from 'react-force-graph';

import VisHeader from '../grid_components/VisHeader';
import { useDashboardFilteredContext } from '../../contexts/DashboardFilteredContext';
// import { useRef } from 'react';


const KnowledgeGraph = () => {
  const { updateFilterOption, dashboardData } = useDashboardFilteredContext();
  const data = dashboardData.knowledgeGraph;

  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className="vis-svg-container">
        <ForceGraph2D
          
          graphData={data.data}
          width={390}
          height={350}
          onNodeClick={(node) => updateFilterOption('keyword', node.id)}
          nodeAutoColorBy="group"
          nodeCanvasObject={(node : any, ctx, globalScale) => {
            const label = node.id;
            const fontSize = 12 / globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

            // add circle with radius proportional to node value
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.value, 0, 2 * Math.PI, false);
            ctx.fillStyle = node.color;
            // add border to circle
            ctx.strokeStyle = 'rgba(255, 0, 255, 1)';
            ctx.lineWidth = 2;
            ctx.fill();


            // ctx.fillStyle = 'rgba(255, 255, 255, 1)';
            // ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
            // // move rect out of the way of the circle
            // ctx.fill();

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = "#000000";
            // move text out of the way of the circle
            ctx.fillText(label, node.x, node.y);


            node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
          }}
          nodePointerAreaPaint={(node, color, ctx) => {
            ctx.fillStyle = color;
            const bckgDimensions = node.__bckgDimensions;
            bckgDimensions && ctx.fillRect(node.x! - bckgDimensions[0] / 2, node.y! - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);
          }}
          nodeVal={node => node.value}
          nodeLabel={node => `${node.id} - ${node.value}`}
          // nodeOpacity={1}
          // nodeThreeObjectExtend={true}
          linkWidth={
            link => {
              const averageLinkValue = data.data.links.reduce((acc, cur) => acc + cur.value, 0) / data.data.links.length;
              return (link.value / averageLinkValue) * 4 + 1;
            }
          }
          // show link labels
          linkLabel={(link : any) => `${link.source?.id} - ${link.target.id}: ${link.value}`}
        />
      </div>
    </div>
  );
};

export default KnowledgeGraph;
