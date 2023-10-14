import { FaStar } from "react-icons/fa";
import { Divider } from "antd";

import VisHeader from "../grid_components/VisHeader";
import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";

export default function SentimentAnalysis() {
  const { updateFilterOption, dashboardData } = useDashboardFilteredContext();
  const data = dashboardData.sentimentAnalysis;
  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div
        className="vis-svg-container"
        style={{ height: 300, overflow: "auto" }}
      >
        {data.data.map((item, index) => (
          <>
            <div
              key={index}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "5px 20px",
              }}
            >
              <div
                style={{ margin: "5px 0" }}
                onClick={() => {
                  switch (item.title) {
                    case "Positive Tweets":
                      updateFilterOption('sentiment', "positive");
                      break;
                    case "Negative Tweets":
                      updateFilterOption('sentiment', "negative");
                      break;
                    case "Neutral Tweets":
                      updateFilterOption('sentiment', "neutral");
                      break;
                    default:
                      updateFilterOption('sentiment', "other");
                  }
                }}
              >
                <p style={{ fontSize: 18 }}>{item.title}</p>
                <p className="text-data">{item.subTitle}</p>
              </div>
              <div style={{ display: "flex" }}>
                <FaStar color="yellow" />
                <p style={{ marginLeft: 10 }}>{item.value}</p>
              </div>
            </div>
            <Divider style={{ margin: "10px 0" }} />
          </>
        ))}
      </div>
    </div>
  );
}
