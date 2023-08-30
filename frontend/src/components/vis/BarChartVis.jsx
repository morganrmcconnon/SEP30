import { useState, useRef, useEffect } from "react";
import arrowAll from "../../assets/arrow-all.svg";
import ColorVar from "../ColorVar";
import dotsVertical from "../../assets/dots-vertical.svg";
import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts";

const data = [
  {
    name: "A",
    Positive: 4000,
    Neutral: 2000,
    Negative: 2400,
    Compound: 2400,
  },
  {
    name: "B",
    Positive: -3000,
    Neutral: 1398,
    Negative: 2400,
    Compound: 2210,
  },
  {
    name: "C",
    Positive: -2000,
    Neutral: -9800,
    Negative: 2400,
    Compound: 2290,
  },
  {
    name: "D",
    Positive: 2780,
    Neutral: 3908,
    Negative: 2400,
    Compound: 2000,
  },
  {
    name: "E",
    Positive: -1890,
    Neutral: 4800,
    Negative: 2400,
    Compound: 2181,
  },
  {
    name: "F",
    Positive: 2390,
    Neutral: -3800,
    Negative: 2400,
    Compound: 2500,
  },
  {
    name: "G",
    Positive: 3490,
    Neutral: 4300,
    Negative: 2400,
    Compound: 2100,
  },
];
const BarChartVis = () => {
  return (
    <div className="vis-container">
      <div className="vis-header">
        <div className="vis-drag-handle">
          <img src={arrowAll} />
        </div>
        <div className="vis-header-title">
          <h3>Bar Chart</h3>
          <p className="text-subtitle">Subtitle</p>
        </div>
        <img className="vis-dots" src={dotsVertical} />
      </div>
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={data}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar dataKey="Positive" fill={ColorVar.blue} />
            <Bar dataKey="Neutral" fill={ColorVar.orange} />
            <Bar dataKey="Negative" fill={ColorVar.red} />
            <Bar dataKey="Compound" fill={ColorVar.green} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BarChartVis;
