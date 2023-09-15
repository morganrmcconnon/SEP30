import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, } from "recharts";

import VisHeader from "../grid_components/VisHeader";
import ColorVar from "../../constants/ColorVar";
import { useSearchContext } from "../../contexts/SearchContext";


const AgeGroupsBarChart = () => {
  const { search, updateSearch, dashboardData } = useSearchContext();
  const data = dashboardData.agegroups;
  return (
    <div className="vis-container">
      <VisHeader title="Age groups" subtitle="Age groups distribution" />
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
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar dataKey="percent" fill={ColorVar.blue} >
              {data.data.map((item, index) => (
                <Cell
                  onClick={() => {
                    updateSearch({ ...search, age: item.name });
                  }}
                  key={`cell-${index}`}
                  fill={item.color}
                  strokeWidth={10}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AgeGroupsBarChart;
