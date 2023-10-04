import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, LabelList, } from "recharts";

import VisHeader from "../grid_components/VisHeader.tsx";
import ColorVar from "../../constants/ColorVar.js";
import { useSearchContext } from "../../contexts/SearchContext.tsx";


const SentimentBarChart = () => {
  const { updateFilterOption, dashboardData } = useSearchContext();
  const data = dashboardData.sentimentAnalysis;
  return (
    <div className="vis-container">
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={data.data}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 30,
            }}
            barCategoryGap={15}
            onClick={(e) => {
              console.log(e);

            } }
            
            
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="title" />
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
