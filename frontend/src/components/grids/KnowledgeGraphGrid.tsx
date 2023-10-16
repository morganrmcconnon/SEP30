// import { ForceGraph2D } from 'react-force-graph';

// import VisHeader from '../grid_components/VisHeader';
// import { useDashboardFilteredContext } from '../../contexts/DashboardFilteredContext';
// // import { useRef } from 'react';


// const KnowledgeGraph = () => {
//   const { updateFilterOption, dashboardData } = useDashboardFilteredContext();
//   const data = dashboardData.knowledgeGraph;

//   return (
//     <div className="vis-container">
//       <VisHeader title={data?.title} subtitle={data?.subTitle} />
//       <div className="vis-svg-container">
//         <ForceGraph2D

//           graphData={data.data}
//           width={390}
//           height={350}
//           onNodeClick={(node) => updateFilterOption('keyword', node.id)}
//           nodeAutoColorBy="group"
//           nodeCanvasObject={(node : any, ctx, globalScale) => {
//             const label = node.id;
//             const fontSize = 12 / globalScale;
//             ctx.font = `${fontSize}px Sans-Serif`;
//             const textWidth = ctx.measureText(label).width;
//             const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

//             // add circle with radius proportional to node value
//             ctx.beginPath();
//             ctx.arc(node.x, node.y, node.value, 0, 2 * Math.PI, false);
//             ctx.fillStyle = node.color;
//             // add border to circle
//             ctx.strokeStyle = 'rgba(255, 0, 255, 1)';
//             ctx.lineWidth = 2;
//             ctx.fill();


//             // ctx.fillStyle = 'rgba(255, 255, 255, 1)';
//             // ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
//             // // move rect out of the way of the circle
//             // ctx.fill();

//             ctx.textAlign = 'center';
//             ctx.textBaseline = 'middle';
//             ctx.fillStyle = "#000000";
//             // move text out of the way of the circle
//             ctx.fillText(label, node.x, node.y);


//             node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
//           }}
//           nodePointerAreaPaint={(node, color, ctx) => {
//             ctx.fillStyle = color;
//             const bckgDimensions = node.__bckgDimensions;
//             bckgDimensions && ctx.fillRect(node.x! - bckgDimensions[0] / 2, node.y! - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);
//           }}
//           nodeVal={node => node.value}
//           nodeLabel={node => `${node.id} - ${node.value}`}
//           // nodeOpacity={1}
//           // nodeThreeObjectExtend={true}
//           linkWidth={
//             link => {
//               const averageLinkValue = data.data.links.reduce((acc, cur) => acc + cur.value, 0) / data.data.links.length;
//               return (link.value / averageLinkValue) * 4 + 1;
//             }
//           }
//           // show link labels
//           linkLabel={(link : any) => `${link.source?.id} - ${link.target.id}: ${link.value}`}
//         />
//       </div>
//     </div>
//   );
// };

// export default KnowledgeGraph;


import { ForceGraph2D } from 'react-force-graph';
import { Space } from 'antd';

import VisHeader from '../grid_components/VisHeader';
import { useDashboardFilteredContext } from '../../contexts/DashboardFilteredContext';
import { ColorVar } from '../../constants/Colors';
// import { useRef } from 'react';

type NodeType = {
  id: string,
  name: string,
  count: number,
  proportion: number,
  value: number,
  group: number,
  color: string,
  selected: boolean,
};

type LinkType = {
  source: string,
  target: string,
  selected: boolean,
  value: number,
};

type GraphDataType = {
  nodes: Array<NodeType>,
  links: Array<LinkType>,
};

const KnowledgeGraph = () => {
  const { filterOptions, updateFilterOption, tweetOjects } = useDashboardFilteredContext();

  const legendList = [
    {
      title: 'Keyword',
      color: ColorVar.blue,
    },
    {
      title: 'Topic',
      color: ColorVar.green,
    }
  ];

  if (filterOptions.keyword !== null || filterOptions.topic !== null) {
    legendList.push({
      title: 'Selected',
      color: ColorVar.red,
    });
  }

  const data: GraphDataType = {
    nodes: [],
    links: [],
  };

  // Count nodes
  tweetOjects.forEach((tweet) => {
    tweet.text_processed.forEach((keyword: string) => {

      const node_found = data.nodes.find((node) => node.name === keyword && node.group === 1);

      if (node_found === undefined) {
        data.nodes.push({
          id: '',
          name: keyword,
          count: 1,
          proportion: 0,
          value: 0,
          group: 1,
          color: ColorVar.blue,
          selected: false,
        });
      } else {
        node_found.value += 1;
      }
    });

    tweet.topic_lda.related_topics.cosine_similarity.forEach((topic: string) => {

      const node_found = data.nodes.find((node) => node.name === topic && node.group === 2);

      if (node_found === undefined) {

        data.nodes.push({
          id: '',
          name: topic,
          count: 1,
          proportion: 0,
          value: 0,
          group: 2,
          selected: false,
          color: ColorVar.green,
        });
      } else {
        node_found.count += 1;
      }
    });
  });

  data.nodes.forEach((node) => {
    node.proportion = node.count / tweetOjects.length;
    node.value = node.proportion * 100;
  });

  // Get only the top 10 keywords and topics
  const top_keywords = data.nodes.filter((node) => node.group === 1).sort((a, b) => b.value - a.value).slice(0, 10);
  const top_topics = data.nodes.filter((node) => node.group === 2).sort((a, b) => b.value - a.value).slice(0, 10);

  data.nodes = [...top_keywords, ...top_topics];

  data.nodes.forEach((node, index) => {
    node.id = index.toString();
  });

  // Count keywords pairs
  tweetOjects.forEach((tweet) => {

    const keywords_list = tweet.text_processed;

    for (let i = 0; i < keywords_list.length; i++) {
      for (let j = i + 1; j < keywords_list.length; j++) {
        if (keywords_list[i] === keywords_list[j]) {
          continue;
        }

        const keyword_smaller = keywords_list[i] < keywords_list[j] ? keywords_list[i] : keywords_list[j];
        const keyword_larger = keywords_list[i] > keywords_list[j] ? keywords_list[i] : keywords_list[j];

        const keyword_smaller_find = data.nodes.find((node) => node.name === keyword_smaller && node.group === 1);
        if (keyword_smaller_find === undefined) {
          continue;
        }
        const keyword_larger_find = data.nodes.find((node) => node.name === keyword_larger && node.group === 1);
        if (keyword_larger_find === undefined) {
          continue;
        }

        const keyword_smaller_id = keyword_smaller_find.id;
        const keyword_larger_id = keyword_larger_find.id;

        const link = data.links.find((link) => link.source === keyword_smaller_id && link.target === keyword_larger_id);
        if (link === undefined) {
          data.links.push({
            source: keyword_smaller_id,
            target: keyword_larger_id,
            selected: true,
            value: 1,
          });
        } else {
          link.value += 1;
        }
      }
    };
  });



  // Count topics pairs
  tweetOjects.forEach((tweet) => {

    const topics_list = tweet.topic_lda.related_topics.cosine_similarity;

    for (let i = 0; i < topics_list.length; i++) {
      for (let j = i + 1; j < topics_list.length; j++) {
        if (topics_list[i] === topics_list[j]) {
          continue;
        }

        const topic_smaller = topics_list[i] < topics_list[j] ? topics_list[i] : topics_list[j];
        const topic_larger = topics_list[i] > topics_list[j] ? topics_list[i] : topics_list[j];

        const topic_smaller_find = data.nodes.find((node) => node.name === topic_smaller && node.group === 2);
        if (topic_smaller_find === undefined) {
          continue;
        }
        const topic_smaller_id = topic_smaller_find.id;

        const topic_larger_find = data.nodes.find((node) => node.name === topic_larger && node.group === 2);
        if (topic_larger_find === undefined) {
          continue;
        }
        const topic_larger_id = topic_larger_find.id;

        const link = data.links.find((link) => link.source === topic_smaller_id && link.target === topic_larger_id);
        if (link === undefined) {
          data.links.push({
            source: topic_smaller_id,
            target: topic_larger_id,
            selected: true,
            value: 1,
          });
        } else {
          link.value += 1;
        }
      }
    };

  });


  // Count keyword-topic pairs
  tweetOjects.forEach((tweet) => {

    const keywords_list = tweet.text_processed;
    const topics_list = tweet.topic_lda.related_topics.cosine_similarity;

    keywords_list.forEach((keyword) => {
      topics_list.forEach((topic) => {
        const keyword_node_found = data.nodes.find((node) => node.name === keyword && node.group === 1);
        const topic_node_found = data.nodes.find((node) => node.name === topic && node.group === 2);

        if (keyword_node_found === undefined || topic_node_found === undefined) {
          return;
        }

        const keyword_id = keyword_node_found.id;
        const topic_id = topic_node_found.id;

        const link = data.links.find((link) => link.source === keyword_id && link.target === topic_id);

        if (link === undefined) {
          data.links.push({
            source: keyword_id,
            target: topic_id,
            selected: true,
            value: 1,
          });
        } else {
          link.value += 1;
        }
      });
    });

    let selected_keyword_id: string | null = null;
    let selected_topic_id: string | null = null;


    if (filterOptions.keyword !== null) {
      const keyword_node = data.nodes.find((node) => node.name === filterOptions.keyword && node.group === 1);
      if (keyword_node !== undefined) {
        keyword_node.selected = true;
        selected_keyword_id = keyword_node.id;
      }
    }

    if (filterOptions.topic !== null) {
      const topic_node = data.nodes.find((node) => node.name === filterOptions.topic && node.group === 2);
      if (topic_node !== undefined) {
        topic_node.selected = true;
        selected_topic_id = topic_node.id;
      }
    }


    data.links = data.links.filter((link) => {
      let link_selected = false;
      if (selected_keyword_id === null && selected_topic_id === null) {
        return true;
      }
      if (selected_keyword_id !== null && (link.source === selected_keyword_id || link.target === selected_keyword_id)) {
        link_selected = true;
      }
      if (selected_topic_id !== null && (link.source === selected_topic_id || link.target === selected_topic_id)) {
        link_selected = true;
      }
      return link_selected;
    });
  });




  return (
    <div className="vis-container">
      <VisHeader title='Knowledge Graph' subtitle='Knowledge Graph' />
      <div className="vis-svg-container">
        <ForceGraph2D

          graphData={data}
          width={390}
          height={280}
          onNodeClick={(node) => {
            if (node.group === 1) {
              updateFilterOption('keyword', node.name);
            }
            if (node.group === 2) {
              updateFilterOption('topic', node.name);
            }
          }}
          nodeColor={(node) => node.color}
          nodeCanvasObject={(node, ctx, globalScale) => {

            // // add circle with radius proportional to node value
            // ctx.beginPath();
            // ctx.arc(node.x!, node.y!, 5 * node.group, 0, 2 * Math.PI, false);
            // ctx.fillStyle = node.color;
            // // add border to circle
            // ctx.strokeStyle = 'rgba(0, 0, 0, 1)';

            // // border size of circle proportional to node value
            // ctx.lineWidth = 1 * node.border_size;
            // // ctx.lineWidth = 200;
            // ctx.fill();




            // // ctx.fillStyle = 'rgba(255, 255, 255, 1)';
            // // ctx.fillRect(node.x! - bckgDimensions[0] / 2, node.y! - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);
            // // // move rect out of the way of the circle
            // // ctx.fill();

            // ctx.textAlign = 'center';
            // ctx.textBaseline = 'middle';
            // ctx.fillStyle = "rgba(0, 0, 0, 0.8)";

            // // Add label
            // ctx.fillText(label, node.x!, node.y!);

            const centerX = node.x!;
            const centerY = node.y!;
            // Map node value from 0 to 100 to radius from 0 to 10
            const radius = 6;

            ctx.beginPath();

            // // Add circle with radius proportional to node value
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
            ctx.fillStyle = node.color;
            ctx.fill();

            if (node.selected) {
              // Add border to radius
              ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
              ctx.lineWidth = 3 / globalScale; // border width
              // Hex color code, but change opacity to 0.5
              ctx.strokeStyle = ColorVar.red;
              ctx.stroke();
            }





            const fontSize = 12 / globalScale;
            const label = node.name;
            const textWidth = ctx.measureText(label).width;


            // Set the text properties


            // Set a transparent black background for the text
            ctx.globalCompositeOperation = 'source-over';



            const padding = 0;
            const bckgDimensions = [textWidth + fontSize * padding / 2, fontSize + fontSize * padding / 2]
            ctx.fillStyle = "rgba(0,0,0, 0.5)"; // Transparent black

            // Draw the text in the middle of the circle
            // const text = "Hello";
            // const textWidth = ctx.measureText(text).width;
            ctx.fillRect(centerX - bckgDimensions[0] / 2, centerY - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);
            ctx.fillStyle = 'white'; // Set the text color back to white
            ctx.font = `${fontSize}px Sans-Serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(label, centerX, centerY, bckgDimensions[0]);

            node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
          }}
          nodePointerAreaPaint={(node, color, ctx) => {
            ctx.fillStyle = color;
            const bckgDimensions = node.__bckgDimensions;
            const centerX = node.x!;
            const centerY = node.y!;
            const radius = 5;
            if (bckgDimensions !== undefined) {
              const backgroundDimensions = [Math.max(2 * radius, bckgDimensions[0]), Math.max(2 * radius, bckgDimensions[1])];
              bckgDimensions && ctx.fillRect(centerX - backgroundDimensions[0] / 2, centerY - backgroundDimensions[1] / 2, backgroundDimensions[0], backgroundDimensions[1]);
            }


          }}
          nodeVal={5}
          nodeLabel={node => `${node.name}: ${node.value}`}
          // nodeOpacity={1}
          // nodeThreeObjectExtend={true}
          linkWidth={5}
          // show link labels
          linkLabel={(link: any) => `${link.source?.name} & ${link.target.name}: ${link.value}`}
        />
        <Space size='large' style={{ marginLeft: 30, marginTop: 20 }}>
          {legendList.map((item, index) => (
            <div style={{ display: 'flex', alignItems: 'center' }} key={index}>
              <div
                style={{
                  width: 6,
                  height: 6,
                  border: '3px solid',
                  borderRadius: '100%',
                  marginRight: 6,
                  borderColor: item.color,
                }}
              />
              <span className='text-data'>{item.title}</span>
            </div>
          ))}
        </Space>
      </div>
    </div>
  );
};

export default KnowledgeGraph;
