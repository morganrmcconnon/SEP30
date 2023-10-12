import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, } from "recharts";

import VisHeader from "../grid_components/VisHeader";
import { ColorVar } from "../../constants/Colors";
import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";


const KeywordsDistribution = () => {
  const { filterOptions: search, updateFilterOptions: updateFilterOption, dashboardData } = useDashboardFilteredContext();
  const griddata = dashboardData.keywordsDistribution;
  const data = griddata.data.sort((a, b) => b.value - a.value);

  return (
    <div className="vis-container">
      <VisHeader title={`Keywords representation of topic`} subtitle={search.topic !== null ? `Probability of the keyword belonging to the topic ${search.topic}` : "Please select a topic to view the keywords distribution"} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          {
            search.topic !== null ?

              <BarChart
                width={500}
                height={300}
                data={data}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 30,
                  left: 40,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey='name' type="category" />
                <Tooltip />
                <Legend />
                <ReferenceLine y={0} stroke="#000" />
                <Bar name="Probability" dataKey="value" fill={ColorVar.blue} >
                  {data.map((item) => (
                    <Cell
                      onClick={() => {
                        updateFilterOption("keyword", item.name);
                      }}
                      strokeWidth={10}
                    />
                  ))}
                </Bar>
              </BarChart>
              : <div className="no-data"></div>}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default KeywordsDistribution;
