import { Responsive, WidthProvider } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import BarChart from "./vis/BarChart";
import PieChart from "./vis/PieChart";
import WordCloud from "./vis/WordCloud";
import Map from "./vis/Map";
import LollipopPlot from "./vis/LollipopPlot";
import "../styles/override.css";

const DashboardVis = () => {
  const ResponsiveGridLayout = WidthProvider(Responsive);

  const items = [
    { i: "BarChart", vis: <BarChart />, x: 0, y: 0, w: 4, h: 1 },
    { i: "Map", vis: <Map />, x: 4, y: 0, w: 2, h: 1 },
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
      >
        {items.map((item) => {
          return (
            <div
              key={item.i}
              style={{ backgroundColor: "#FFFFFF" }}
              data-grid={{ x: item.x, y: item.y }}
            >
              {item.vis}
            </div>
          );
        })}
      </ResponsiveGridLayout>
    </div>
  );
};

export default DashboardVis;
