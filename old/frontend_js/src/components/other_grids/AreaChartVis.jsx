import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, } from "recharts";

import VisHeader from "../grid_components/VisHeader";
import ColorVar from "../../constants/ColorVar";

const data = [
  {
    name: "A",
    Positive: 4000,
    Neutral: 2400,
    Negative: 2400,
  },
  {
    name: "B",
    Positive: 3000,
    Neutral: 1398,
    Negative: 2210,
  },
  {
    name: "C",
    Positive: 2000,
    Neutral: 9800,
    Negative: 2290,
  },
  {
    name: "D",
    Positive: 2780,
    Neutral: 3908,
    Negative: 2000,
  },
  {
    name: "E",
    Positive: 1890,
    Neutral: 4800,
    Negative: 2181,
  },
  {
    name: "F",
    Positive: 2390,
    Neutral: 3800,
    Negative: 2500,
  },
  {
    name: "G",
    Positive: 3490,
    Neutral: 4300,
    Negative: 2100,
  },
];
const AreaChartVis = () => {
  return (
    <div className="vis-container">
      <VisHeader title="Area Chart" subtitle="AreaChart Subtitle" />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            width={500}
            height={400}
            data={data}
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="Positive"
              stackId="1"
              stroke={ColorVar.blue}
              fill={ColorVar.blue}
            />
            <Area
              type="monotone"
              dataKey="Neutral"
              stackId="1"
              stroke={ColorVar.orange}
              fill={ColorVar.orange}
            />
            <Area
              type="monotone"
              dataKey="Negative"
              stackId="1"
              stroke={ColorVar.red}
              fill={ColorVar.red}
            />
            <Legend />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AreaChartVis;
