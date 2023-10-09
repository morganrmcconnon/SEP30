import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, LabelList, } from "recharts";

import VisHeader from "../grid_components/VisHeader.tsx";
import { ColorMap, ColorVar } from "../../constants/Colors.js";
import { useSearchContext } from "../../contexts/SearchContext.tsx";


const SentimentBarChart = () => {
  const { updateFilterOption, dashboardData } = useSearchContext();
  const griddata = dashboardData.genders;
  const data = [
    { id: 'female', title: "Female", color: ColorMap.female.normal, value: griddata.data.female.present },
    { id: 'male', title: "Male", color: ColorMap.male.normal, value: griddata.data.male.present },
  ];
  return (
    <div className="vis-container">
      <VisHeader title={griddata?.title} subtitle={griddata?.subTitle} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={data}
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
            <Bar name="Tweets per Gender" dataKey="value" fill={ColorVar.blue} >
              {data.map((item, index) => (
                <>
                <LabelList
                    dataKey="value"
                    position="top"
                    angle={0}
                    offset={5}
                  />
                
                <Cell
                  onClick={() => {
                    updateFilterOption("gender", item.id);
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