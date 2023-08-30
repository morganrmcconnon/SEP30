import { Responsive, WidthProvider } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import BarChart from "./vis/BarChart";
import PieChart from "./vis/PieChart";
import WordCloud from "./vis/WordCloud";
import Map from "./vis/Map";
import LollipopChart from "./vis/LollipopChart";
import "../styles/override.css";
import { TestRoBERTa, TestVader } from "./MyPost";

const DashboardVis = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { i: "BarChart", vis: <BarChart />, x: 0, y: 0, w: 4, h: 2 },
    { i: "Map", vis: <Map />, x: 4, y: 0, w: 3, h: 3 },
    { i: "PieChart", vis: <PieChart />, x: 4, y: 0, w: 3, h: 3 },
    { i: "SentimentRoBERTa", vis: <TestRoBERTa />, x: 0, y: 4, w: 3, h: 2 },
    { i: "SentimentVader", vis: <TestVader />, x: 4, y: 4, w: 3, h: 2 },
  ];
  return (
    <div>
      <h2>Dashboard</h2>
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
    </div>
  );
};

export default DashboardVis;
