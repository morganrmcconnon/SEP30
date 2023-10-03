import { Responsive, WidthProvider } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "../styles/override.css";

import DemoRoBERTa from "./grids/DemoRoBERTa.tsx";
import DemoVader from "./grids/DemoVader.tsx";

const AboutGrids = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { i: "DemoRoBERTa", vis: <DemoRoBERTa />, x: 8, y: 4, w: 4, h: 1.5 },
    { i: "DemoVader", vis: <DemoVader />, x: 8, y: 4, w: 4, h: 1.5 },
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
