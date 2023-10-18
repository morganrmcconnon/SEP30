import { Responsive, WidthProvider } from "react-grid-layout";

import "react-grid-layout/css/styles.css";
import "../../styles/override.css";

import RealTimeAnalysisGrid from "../grids/RealTimeAnalysisGrid.tsx";
// import SentimentAnalysisGrid from "./grids/SentimentAnalysisGrid.tsx";
import SentimentBarChartGrid from "../grids/SentimentBarChartGrid.tsx";
import TopicsTable from "../grids/TopicsTable.tsx";
import TopicsCountBarChart from "../grids/TopicsCountBarChart.tsx";
import KeywordsCountBarChart from "../grids/KeywordsCountBarChart.tsx";
import AgeGroupsBarChart from "../grids/AgeGroupsBarChartGrid.tsx";
import AgeGroupsGrid from "../grids/AgeGroupsPieChartGrid.tsx";
import AgeGroupsWeekly from "../grids/AgeGroupsWeeklyGrid.tsx";
import SentimentGroupsWeekly from "../grids/SentimentGroupsWeeklyGrid.tsx";
import GenderGroupsWeekly from "../grids/GenderGroupsWeeklyGrid.tsx";
import GendersGrid from "../grids/GendersGrid.tsx";
import GendersPieChartGrid from "../grids/GendersPieChartGrid.tsx";
import GendersBarChartGrid from "../grids/GendersBarChartGrid.tsx"
import LocationsGrid from "../grids/LocationsGrid.tsx";
import KnowledgeGraph from "../grids/KnowledgeGraphGrid.tsx";
// import TestEndpoint from "./grids/TestEndpoint.tsx";
// import FilterOptionsGrid from "./grids/FilterOptionsGrid.tsx";

const DashboardVis = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  //Defines initial size and location of vis components in dashboard
  //vis defines the component that will be mapped in dashboard render
  const items = [
    { y: 0, x: 0, w: 8, h: 2.7, i: "RealTimeAnalysis", vis: <RealTimeAnalysisGrid /> },
    { y: 0, x: 8, w: 4, h: 2.7, i: "KnowledgeGraph", vis: <KnowledgeGraph /> },
    { y: 1, x: 0, w: 4, h: 2.7, i: "AgeGroupsWeekly", vis: <AgeGroupsWeekly /> },
    { y: 1, x: 4, w: 4, h: 2.7, i: "SentimentGroupsWeekly", vis: <SentimentGroupsWeekly /> },
    { y: 1, x: 8, w: 4, h: 2.7, i: "GenderGroupsWeekly", vis: <GenderGroupsWeekly /> },
    { y: 2, x: 0, w: 4, h: 2.7, i: "SentimentBarChart", vis: <SentimentBarChartGrid /> },
    { y: 2, x: 4, w: 4, h: 2.7, i: "AgeGroupsBarChart", vis: <AgeGroupsBarChart /> },
    { y: 2, x: 8, w: 4, h: 2.7, i: "AgeGroups", vis: <AgeGroupsGrid /> },
    { y: 3, x: 0, w: 4, h: 2.7, i: "TopicsTable", vis: <TopicsTable /> },
    { y: 3, x: 4, w: 4, h: 2.7, i: "TopicsCountBarChart", vis: <TopicsCountBarChart /> },
    { y: 3, x: 8, w: 4, h: 2.7, i: "KeywordsCountBarChart", vis: <KeywordsCountBarChart /> },
    { y: 4, x: 0, w: 4, h: 2.7, i: "GendersPieChartGrid", vis: <GendersPieChartGrid /> },
    { y: 4, x: 4, w: 4, h: 2.7, i: "GendersBarChartGrid", vis: <GendersBarChartGrid /> },
    { y: 4, x: 8, w: 4, h: 2.7, i: "Genders", vis: <GendersGrid /> },
    { y: 5, x: 0, w: 8, h: 2.7, i: "Locations", vis: <LocationsGrid /> },
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
