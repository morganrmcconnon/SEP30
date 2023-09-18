import { Responsive, WidthProvider } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "../styles/override.css";

import RealTimeAnalysisGrid from "./grids/RealTimeAnalysisGrid";
import SentimentAnalysisGrid from "./grids/SentimentAnalysisGrid";
import SentimentPieChartGrid from "./grids/SentimentPieChartGrid";
import TopicModellingGrid from "./grids/TopicModellingGrid";
import KeywordsDistribution from "./grids/KeywordsDistributionGrid";
import AgeGroupsBarChart from "./grids/AgeGroupsBarChartGrid";
import AgeGroupsGrid from "./grids/AgeGroupsGrid";
import GendersGrid from "./grids/GendersGrid";
import GendersPieChartGrid from "./grids/GendersPieChartGrid";
import LocationsGrid from "./grids/LocationsGrid";
import KnowledgeGraph from "./grids/KnowledgeGraphGrid";
import TestEndpoint from "./grids/TestEndpoint";
import FilterOptionsGrid from "./grids/FilterOptionsGrid";
import DemoRoBERTa from "./grids/DemoRoBERTa";
import DemoVader from "./grids/DemoVader";

const DashboardVis = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { i: "RealTimeAnalysis", vis: <RealTimeAnalysisGrid />, x: 0, y: 0, w: 8, h: 3, },
    { i: "AgeGroups", vis: <AgeGroupsGrid />, x: 8, y: 0, w: 4, h: 3 },
    { i: "AgeGroupsBarChart", vis: <AgeGroupsBarChart />, x: 0, y: 1, w: 4, h: 3 },
    { i: "SentimentAnalysis", vis: <SentimentAnalysisGrid />, x: 4, y: 1, w: 4, h: 3, },
    { i: "SentimentPieChart", vis: <SentimentPieChartGrid />, x: 8, y: 1, w: 4, h: 3 },
    { i: "GendersPieChartGrid", vis: <GendersPieChartGrid />, x: 0, y: 2, w: 4, h: 3 },
    { i: "TopicModelling", vis: <TopicModellingGrid />, x: 4, y: 2, w: 4, h: 3 },
    { i: "KeywordsDistribution", vis: <KeywordsDistribution />, x: 8, y: 2, w: 4, h: 3 },
    { i: "Genders", vis: <GendersGrid />, x: 0, y: 4, w: 4, h: 3 },
    { i: "KnowledgeGraph", vis: <KnowledgeGraph />, x: 4, y: 3, w: 4, h: 3 },
    { i: "TestEndpoint", vis: <TestEndpoint />, x: 8, y: 3, w: 4, h: 1.3 },
    { i: "FilterOptionsGrid", vis: <FilterOptionsGrid />, x: 8, y: 4, w: 4, h: 1.7 },
    { i: "Locations", vis: <LocationsGrid />, x: 0, y: 4, w: 8, h: 3 },
    { i: "TestRoBERTa", vis: <DemoRoBERTa />, x: 8, y: 4, w: 4, h: 1.5 },
    { i: "TestVader", vis: <DemoVader />, x: 8, y: 4, w: 4, h: 1.5 },
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

export default DashboardVis;
