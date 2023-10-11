import { Responsive, WidthProvider } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "../styles/override.css";

import DemoTranslate from "./grids/DemoTranslate.tsx";
import DemoFilterTweetsSpacy from "./grids/DemoFilterTweetsSpacy.tsx";
import DemoSentimentRoBERTa from "./grids/DemoSentimentRoBERTa.tsx";
import DemoTopicLDA from "./grids/DemoTopicLDA.tsx";
import DemoTopicBERTArxiv from "./grids/DemoTopicBERTArxiv.tsx";
import DemoTopicCardiffNLP from "./grids/DemoTopicCardiffNLP.tsx";
import DemoLocation from "./grids/DemoLocation.tsx";
import DemoM3Inference from "./grids/DemoM3Inference.tsx";

const AboutGrids = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { y: 0, x: 0, w: 4, h: 2, i: "DemoTranslate", vis: <DemoTranslate /> },
    { y: 0, x: 4, w: 4, h: 2, i: "DemoFilterTweetsSpacy", vis: <DemoFilterTweetsSpacy /> },
    { y: 0, x: 8, w: 4, h: 2, i: "DemoSentimentRoBERTa", vis: <DemoSentimentRoBERTa /> },
    { y: 1, x: 0, w: 4, h: 2, i: "DemoTopicLDA", vis: <DemoTopicLDA /> },
    { y: 1, x: 4, w: 4, h: 2, i: "DemoTopicBERTArxiv", vis: <DemoTopicBERTArxiv /> },
    { y: 1, x: 8, w: 4, h: 2, i: "DemoTopicCardiffNLP", vis: <DemoTopicCardiffNLP /> },
    { y: 2, x: 0, w: 4, h: 2, i: "DemoGeopy", vis: <DemoLocation /> },
    { y: 2, x: 4, w: 4, h: 2, i: "DemoM3Inference", vis: <DemoM3Inference /> },
  ];
  return (
    <ResponsiveGridLayout
      className="layout"
      layouts={{ lg: items }}
      breakpoints={{ lg: 1200, md: 996, sm: 768 }}
      cols={{ lg: 12, md: 10, sm: 6 }}
      isResizable={false}
      //Determines which className controls draggable handle for components
      draggableHandle=".vis-drag-handle"
    >
      {items.map((item) => {
        //Renders each vis component as defined in items array
        return (
          <div key={item.i} data-grid={{ x: item.x, y: item.y }}>
            {item.vis}
          </div>
        );
      })}
    </ResponsiveGridLayout>
  );
};

export default AboutGrids;
