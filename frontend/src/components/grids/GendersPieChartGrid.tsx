import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Col, Row } from "antd";

import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";
import VisHeader from "../grid_components/VisHeader";
import { ColorVar } from "../../constants/Colors";

export default function GendersPieChartGrid() {

  const { updateFilterOption, dashboardData } = useDashboardFilteredContext();
  const griddata = dashboardData.genders;
  const data = [
    { id: 'female', title: "Female", color: ColorVar.red, value: griddata.data.female.present },
    { id: 'male', title: "Male", color: ColorVar.blue, value: griddata.data.male.present },
  ];

  return (
    <div className="vis-container">
      <VisHeader title={griddata?.title} subtitle={griddata?.subTitle} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height={262}>
          <PieChart >
            <Pie 
              dataKey="value"
              data={data}
              //Determines y coord offset
              cy={130}
              innerRadius={0}
              outerRadius={100}
              fill="#82ca9d"
              startAngle={-270}
              endAngle={90}
            >
              {data.map((item, index) => (
                <Cell 
                  onClick={() => {
                    updateFilterOption('gender', item.id);
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
                {item?.title} ({item?.value})
              </p>
            </Col>
          ))}
        </Row>
      </div>
    </div>
  );
}
