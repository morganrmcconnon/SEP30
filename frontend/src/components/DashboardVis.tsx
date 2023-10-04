import { Responsive, WidthProvider } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "../styles/override.css";

import RealTimeAnalysisGrid from "./grids/RealTimeAnalysisGrid.tsx";
// import SentimentAnalysisGrid from "./grids/SentimentAnalysisGrid.tsx";
import SentimentBarChartGrid from "./grids/SentimentBarChartGrid.tsx";
import TopicModellingGrid from "./grids/TopicModellingGrid.tsx";
// import KeywordsDistribution from "./grids/KeywordsDistributionGrid.tsx";
import AgeGroupsBarChart from "./grids/AgeGroupsBarChartGrid.tsx";
import AgeGroupsGrid from "./grids/AgeGroupsGrid.tsx";
import AgeGroupsWeekly from "./grids/AgeGroupsWeeklyGrid.tsx";
import SentimentGroupsWeekly from "./grids/SentimentGroupsWeeklyGrid.tsx";
import GenderGroupsWeekly from "./grids/GenderGroupsWeeklyGrid.tsx";
import GendersGrid from "./grids/GendersGrid.tsx";
import GendersPieChartGrid from "./grids/GendersPieChartGrid.tsx";
import GendersBarChartGrid from "./grids/GendersBarChartGrid.tsx"
import LocationsGrid from "./grids/LocationsGrid.tsx";
import KnowledgeGraph from "./grids/KnowledgeGraphGrid.tsx";
// import TestEndpoint from "./grids/TestEndpoint.tsx";
// import FilterOptionsGrid from "./grids/FilterOptionsGrid.tsx";

const DashboardVis = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { i: "AgeGroupsWeekly", vis: <AgeGroupsWeekly/>, x: 0, y: 0, w: 4, h: 2.7, },
    { i: "SentimentGroupsWeekly", vis: <SentimentGroupsWeekly/>, x: 4, y: 0, w: 4, h: 2.7, },
    { i: "GenderGroupsWeekly", vis: <GenderGroupsWeekly/>, x: 8, y: 0, w: 4, h: 2.7, },
    { i: "RealTimeAnalysis", vis: <RealTimeAnalysisGrid />, x: 0, y: 1, w: 8, h: 3, },
    { i: "AgeGroups", vis: <AgeGroupsGrid />, x: 8, y: 3, w: 4, h: 3 },
    { i: "AgeGroupsBarChart", vis: <AgeGroupsBarChart />, x: 0, y: 1, w: 4, h: 3 },
    { i: "SentimentBarChart", vis: <SentimentBarChartGrid />, x: 8, y: 1, w: 4, h: 3 },
    { i: "GendersPieChartGrid", vis: <GendersPieChartGrid />, x: 0, y: 3, w: 4, h: 3 },
    { i: "GendersBarChartGrid", vis: <GendersBarChartGrid />, x: 4, y: 3, w: 4, h: 3 },
    { i: "TopicModelling", vis: <TopicModellingGrid />, x: 4, y: 2, w: 4, h: 3 },
    { i: "KnowledgeGraph", vis: <KnowledgeGraph />, x: 4, y: 3, w: 4, h: 3 },
    { i: "Genders", vis: <GendersGrid />, x: 8, y: 3, w: 4, h: 3 },
    { i: "Locations", vis: <LocationsGrid />, x: 4, y: 4, w: 8, h: 3 },
    // { i: "SentimentAnalysis", vis: <SentimentAnalysisGrid />, x: 4, y: 1, w: 4, h: 3, },
    // { i: "KeywordsDistribution", vis: <KeywordsDistribution />, x: 8, y: 2, w: 4, h: 3 },
    //{ i: "TestEndpoint", vis: <TestEndpoint />, x: 8, y: 3, w: 4, h: 1.3 },
    //{ i: "FilterOptionsGrid", vis: <FilterOptionsGrid />, x: 8, y: 4, w: 4, h: 1.7 },
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
