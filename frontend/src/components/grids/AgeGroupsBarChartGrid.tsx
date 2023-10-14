import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, LabelList, } from "recharts";

import VisHeader from "../grid_components/VisHeader";
import { ColorMap, ColorVar } from "../../constants/Colors.js";
import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext.tsx";
import { AgeGroupData, AgeGroupValue } from "../../data/api/types/constants.ts";


const AgeGroupsBarChart = () => {
  const { updateFilterOption, tweetOjects } = useDashboardFilteredContext();
  
  const age_group_count : AgeGroupData<{
    key: AgeGroupValue,
    name: string,
    count: number,
    proportion: number,
    color: string,
  }> = {
    "<=18": {
      key: "<=18",
      name: "Under 18",
      count: 0,
      proportion: 0,
      color: ColorMap["<=18"],
    },
    "19-29": {
      key: "19-29",
      name: "19-29",
      count: 0,
      proportion: 0,
      color: ColorMap["19-29"],
    },
    "30-39": {
      key: "30-39",
      name: "30-39",
      count: 0,
      proportion: 0,
      color: ColorMap["30-39"],
    },
    ">=40": {
      key: ">=40",
      name: "40 and above",
      count: 0,
      proportion: 0,
      color: ColorMap[">=40"],
    },
  };
  
  tweetOjects.forEach((tweet) => {
    age_group_count[tweet.user.age].count += 1;
  });

  Object.entries(age_group_count).forEach(([age_group, value]) => {
    age_group_count[age_group as AgeGroupValue].proportion = tweetOjects !== undefined ? value.count / tweetOjects.length : 0;
  });


  const data = Object.values(age_group_count);

  return (
    <div className="vis-container">
      <VisHeader title="Demographic Analysis - Age groups" subtitle="Age groups distribution" />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 0,
              bottom: 30,
            }}
            barCategoryGap={10}
            barSize={50}
            key={Math.random()}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" interval={0} fontSize={10} />
            <YAxis />
            <Tooltip />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar dataKey="count" name="Tweets per Age group" fill={ColorVar.blue} >
              {data.map((item, index) => (
                <>
                  <LabelList
                    dataKey="count"
                    position="top"
                    angle={0}
                    offset={5}
                    key={item.key}
                  />
                  <Cell
                    onClick={() => {updateFilterOption("age", item.key);}}
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

export default AgeGroupsBarChart;
