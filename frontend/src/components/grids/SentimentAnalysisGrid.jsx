import React from "react";
import { FaStar } from "react-icons/fa";
import { Divider } from "antd";

import VisHeader from "../grid_components/VisHeader";
import { useSearchContext } from "../../contexts/SearchContext";
import DATATYPES from "../../constants/dataTypes";


export default function SentimentAnalysis() {
  const { search, updateSearch, dashboardData } = useSearchContext();
  const data = dashboardData.sentimentAnalysis;
  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div
        className="vis-svg-container"
        style={{ height: 350, overflow: "auto" }}
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
                      updateSearch({ ...search, sentiment: "Positive" });
                      break;
                    case "Negative Tweets":
                      updateSearch({ ...search, sentiment: "Negative" });
                      break;
                    case "Neutral Tweets":
                      updateSearch({ ...search, sentiment: "Neutral" });
                      break;
                    default:
                      updateSearch({ ...search, sentiment: "Other" });
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
