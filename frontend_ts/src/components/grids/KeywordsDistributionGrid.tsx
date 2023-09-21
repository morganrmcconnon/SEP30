import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, } from "recharts";

import VisHeader from "../grid_components/VisHeader";
import ColorVar from "../../constants/ColorVar";
import { useSearchContext } from "../../contexts/SearchContext";


const KeywordsDistribution = () => {
  const { search, updateSearch, dashboardData } = useSearchContext();
  const griddata = dashboardData.keywordsDistribution;
  const data = griddata.data.sort((a, b) => b.value - a.value);

  return (
    <div className="vis-container">
      <VisHeader title={griddata?.title} subtitle={`Keywords distribution of Topic ${search.topic}`} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={data}
            layout="vertical"
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey='name' type="category" />
            <Tooltip />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar dataKey="value" fill={ColorVar.blue} >
              {data.map((item) => (
                <Cell
                  onClick={() => {
                    updateSearch({ ...search, keyword: item.name });
                  }}
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

export default KeywordsDistribution;
