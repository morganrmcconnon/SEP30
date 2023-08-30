import { useState, useRef, useEffect } from "react";
import arrowAll from "../../assets/arrow-all.svg";
import dotsVertical from "../../assets/dots-vertical.svg";
import ColorVar from "../ColorVar";
import { Cell, Tooltip, PieChart, Pie, ResponsiveContainer } from "recharts";

const PieChartVis = () => {
  const data = [
    { name: "Group A", value: 400 },
    { name: "Group B", value: 300 },
    { name: "Group C", value: 300 },
    { name: "Group D", value: 200 },
  ];

  const COLORS = [
    `${ColorVar.blue}`,
    `${ColorVar.green}`,
    `${ColorVar.red}`,
    `${ColorVar.orange}`,
  ];

  return (
    <div className="vis-container">
      <div className="vis-header">
        <div className="vis-drag-handle">
          <img src={arrowAll} />
        </div>
        <div className="vis-header-title">
          <h3>Pie Chart</h3>
          <p className="text-subtitle">Subtitle</p>
        </div>
        <img className="vis-dots" src={dotsVertical} />
      </div>
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              dataKey="value"
              data={data}
              //Determines y coord offset
              cy={175}
              innerRadius={60}
              outerRadius={120}
              fill="#82ca9d"
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PieChartVis;
