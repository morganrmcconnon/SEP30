import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, LabelList, } from "recharts";

import VisHeader from "../grid_components/VisHeader.tsx";
import { ColorVar } from "../../constants/Colors.js";
import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext.tsx";


const SentimentBarChart = () => {
  const { updateFilterOption: updateFilterOption, dashboardData } = useDashboardFilteredContext();
  const data = dashboardData.sentimentAnalysis;
  return (
    <div className="vis-container">
      <VisHeader title='Sentiment Analysis' subtitle='Tweets distribution by sentiment' />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={data.data}
            margin={{
              top: 20,
              right: 30,
              left: 0,
              bottom: 30,
            }}
            barCategoryGap={15}
            key={Math.random()}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="title" interval={0} fontSize={12} />
            <YAxis />
            <Tooltip />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar name="Tweets" dataKey="value" fill={ColorVar.blue} >
              {data.data.map((item, index) => (
                <>
                <LabelList
                    dataKey="value"
                    position="top"
                    angle={0}
                    offset={5}
                  />
                
                <Cell
                  onClick={() => {
                    updateFilterOption("sentiment", item.value_key);
                  }}
                  key={`cell-${index}`}
                  fill={item.color}
                  strokeWidth={10}
                />
                </>
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SentimentBarChart;
