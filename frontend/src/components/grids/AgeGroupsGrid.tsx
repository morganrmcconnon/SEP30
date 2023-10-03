import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Col, Row } from "antd";

import { SearchProvider, useSearchContext } from "../../contexts/SearchContext";
import VisHeader from "../grid_components/VisHeader";

export default function AgeGroups() {
  const { updateFilterOption, dashboardData } = useSearchContext();
  const data = dashboardData.agegroups;
  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className="vis-svg-container">
        <SearchProvider>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                dataKey="percent"
                data={data.data}
                cy={130}
                innerRadius={60}
                outerRadius={100}
                fill="#82ca9d"    
                startAngle={-270}
                endAngle={90}
              >
                {data.data.map((item, index) => (
                  <Cell
                    onClick={() => {
                      updateFilterOption("age", item.id);
                    }}
                    key={`cell-${index}`}
                    fill={item.color}
                    strokeWidth={1}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </SearchProvider>
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
