import { Responsive, WidthProvider } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import BarChart from "./vis/BarChart";
import PieChart from "./vis/PieChartVis";
import WordCloud from "./vis/WordCloud";
import LineChartVis from "./vis/LineChartVis";
import Map from "./vis/Map";
import LollipopChart from "./vis/LollipopChart";
import "../styles/override.css";
import { TestRoBERTa, TestVader } from "./MyPost";
import BarChartVis from "./vis/BarChartVis";
import AreaChartVis from "./vis/AreaChartVis";
import KnowledgeGraph from "./vis/KnowledgeGraph";
import CounterCard from "./testcontext/CounterCard";
import ResultCard from "./testcontext/ResultCard";
import { CounterProvider } from "./testcontext/CounterContext";
import DemographicAnalysis from "./DemographicAnalysis";
import TopTrends from "./TopTrends";
import TopicModelling from "./TopicModelling";
import SentimentAnalysis from "./SentimentAnalysis";
import DemoGraphic1 from "./DemoGraphic1";
import DemoGraphic2 from "./DemoGraphic2";
import DemoGraphic3 from "./DemoGraphic3";
import { SearchProvider, useSearch } from "./SearchContext";

const DashboardVis = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    {
      i: "DemographicAnalysis",
      vis: <DemographicAnalysis />,
      x: 0,
      y: 0,
      w: 8,
      h: 3,
    },
    { i: "TopTrends", vis: <TopTrends />, x: 8, y: 0, w: 4, h: 3 },
    { i: "TopicModelling", vis: <TopicModelling />, x: 0, y: 1, w: 4, h: 3 },
    {
      i: "SentimentAnalysis",
      vis: <SentimentAnalysis />,
      x: 4,
      y: 1,
      w: 4,
      h: 3,
    },
    { i: "DemoGraphic1", vis: <DemoGraphic1 />, x: 8, y: 1, w: 4, h: 3 },
    { i: "DemoGraphic2", vis: <DemoGraphic2 />, x: 0, y: 2, w: 4, h: 3 },
    { i: "DemoGraphic3", vis: <DemoGraphic3 />, x: 4, y: 2, w: 8, h: 3 },
    { i: "BarChartVis", vis: <BarChartVis />, x: 0, y: 5, w: 3, h: 3 },
    { i: "LineChartVis", vis: <LineChartVis />, x: 3, y: 5, w: 3, h: 3 },
    { i: "PieChart", vis: <PieChart />, x: 6, y: 5, w: 2, h: 3 },
    { i: "AreaChartVis", vis: <AreaChartVis />, x: 9, y: 5, w: 4, h: 3 },
    { i: "SentimentRoBERTa", vis: <TestRoBERTa />, x: 0, y: 8, w: 3, h: 2 },
    { i: "SentimentVader", vis: <TestVader />, x: 3, y: 8, w: 3, h: 2 },
    { i: "Counter", vis: <CounterCard />, x: 6, y: 8, w: 3, h: 2 },
    { i: "Card", vis: <ResultCard />, x: 9, y: 8, w: 3, h: 2 },
    { i: "KnowledgeGraph", vis: <KnowledgeGraph />, x: 0, y: 10, w: 5, h: 3 },
    { i: "BarChart", vis: <BarChart />, x: 5, y: 10, w: 4, h: 2 },
  ];
  return (
    <div>
      <h2>Dashboard</h2>
      <CounterProvider>
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
      </CounterProvider>
    </div>
  );
};

export default DashboardVis;
