import { Responsive, WidthProvider } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "../../styles/override.css";

import DemoTranslate from "../about_grids/DemoTranslate.tsx";
import DemoTextProcessed from "../about_grids/DemoTextProcessed.tsx";
import DemoSentimentRoBERTa from "../about_grids/DemoSentimentRoBERTa.tsx";
import DemoTopicLDA from "../about_grids/DemoTopicLDA.tsx";
import DemoTopicBERTArxiv from "../about_grids/DemoTopicBERTArxiv.tsx";
import DemoTopicCardiffNLP from "../about_grids/DemoTopicCardiffNLP.tsx";
import DemoLocation from "../about_grids/DemoLocation.tsx";
import DemoM3Inference from "../about_grids/DemoM3Inference.tsx";
import DemoFilterTweetsSpacy from "../about_grids/DemoFilterTweetsSpacy.tsx";

const AboutGrids = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { y: 0, x: 0, w: 4, h: 2, i: "DemoTranslate", vis: <DemoTranslate /> },
    { y: 0, x: 4, w: 4, h: 2, i: "DemoFilterTweetsSpacy", vis: <DemoFilterTweetsSpacy /> },
    { y: 0, x: 8, w: 4, h: 2, i: "DemoTextProcessed", vis: <DemoTextProcessed /> },
    { y: 0, x: 0, w: 4, h: 2, i: "DemoSentimentRoBERTa", vis: <DemoSentimentRoBERTa /> },
    { y: 0, x: 4, w: 4, h: 2, i: "DemoTopicLDA", vis: <DemoTopicLDA /> },
    { y: 0, x: 8, w: 4, h: 2, i: "DemoTopicBERTArxiv", vis: <DemoTopicBERTArxiv /> },
    { y: 0, x: 0, w: 4, h: 2, i: "DemoTopicCardiffNLP", vis: <DemoTopicCardiffNLP /> },
    { y: 0, x: 4, w: 4, h: 2, i: "DemoGeopy", vis: <DemoLocation /> },
    { y: 0, x: 8, w: 4, h: 2, i: "DemoM3Inference", vis: <DemoM3Inference /> },
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
