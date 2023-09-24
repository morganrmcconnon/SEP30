import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Col, Row } from "antd";

import { useSearchContext } from "../../contexts/SearchContext";
import VisHeader from "../grid_components/VisHeader";

export default function SentimentPieChartGrid() {

  const { updateFilterOption, dashboardData } = useSearchContext();
  const data = dashboardData.sentimentAnalysis;

  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie
              dataKey="value"
              data={data.data}
              //Determines y coord offset
              cy={130}
              innerRadius={0}
              outerRadius={100}
              fill="#82ca9d"
              startAngle={-270}
              endAngle={90}
            >
              {data.data.map((item, index) => (
                <Cell
                  onClick={() => {
                    updateFilterOption('sentiment', item.value_key);
                  }}
                  key={`cell-${index}`}
                  fill={item.color}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
        <Row style={{ margin: "20px" }}>
          {data.data.map((item, index) => (
            <Col
              span={12}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: 18,
              }}
              key={index}
            >
              <div
                style={{
                  width: 6,
                  height: 6,
                  border: "3px solid",
                  borderRadius: "100%",
                  marginRight: 6,
                  borderColor: item.color,
                }}
              />
              <p>
                {item?.title} ({item?.value})
              </p>
            </Col>
          ))}
        </Row>
      </div>
    </div>
  );
}
