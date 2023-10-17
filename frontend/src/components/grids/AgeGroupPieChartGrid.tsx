import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Col, Row } from "antd";

import { DashboardFilteredContextProvider, useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";
import VisHeader from "../grid_components/VisHeader";

export default function AgeGroups() {
  const { updateFilterOption, dashboardData } = useDashboardFilteredContext();
  const data = dashboardData.agegroups.data.slice().sort((a, b) => b.percent - a.percent);
  return (
    <div className="vis-container">
      <VisHeader title='Demographic Analysis - Age Groups' subtitle='Proportion of tweets by age groups' />
      <div className="vis-svg-container">
        <DashboardFilteredContextProvider>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                dataKey="percent"
                data={data}
                cy={130}
                innerRadius={60}
                outerRadius={100}
                fill="#82ca9d"    
                startAngle={-270}
                endAngle={90}
              >
                {data.map((item) => (
                  <Cell
                    onClick={() => {updateFilterOption("age", item.key);}}
                    key={`cell-${item.key}`}
                    fill={item.color}
                    strokeWidth={1}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </DashboardFilteredContextProvider>
        <Row style={{ margin: "20px" }}>
          {data.map((item, index) => (
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
              <p className="text-data">
                {item?.name} ({item?.percent}%)
              </p>
            </Col>
          ))}
        </Row>
      </div>
    </div>
  );
}