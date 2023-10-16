import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer, LabelList, } from "recharts";
import { TooltipProps } from 'recharts';
import {
  ValueType,
  NameType,
} from 'recharts/types/component/DefaultTooltipContent';

import VisHeader from "../grid_components/VisHeader";
import { ColorVar } from "../../constants/Colors";
import { useDashboardFilteredContext } from "../../contexts/DashboardFilteredContext";

const CustomTooltip = ({ active, payload, label }: TooltipProps<ValueType, NameType>) => {
  if (active && payload && payload.length) {
    const item = payload[0].payload;
    return (
      <div style={{ backgroundColor: 'white', padding: 8, border: '1px solid black' }}>
        <p>{`"${label}"`}</p>
        <p>Occured in {item.count} tweets ({Math.round(item.proportion * 10000) / 100}%)</p>
        <p>Mentioned {item.frequency} times</p>
      </div>
    );
  }

  return null;
};

const KeywordsCountBarChart = () => {
  const { filterOptions, updateFilterOption, tweetOjects } = useDashboardFilteredContext();

  const keywords_count : Record<string,{
    count: number,
    frequency: number,
  }> = {};

  tweetOjects?.forEach((tweet) => {
    const unique_words = new Set();
    tweet.text_processed.forEach((word) => {
      if (keywords_count.hasOwnProperty(word) === false) {
        keywords_count[word] = {
          count: 0,
          frequency: 0,
        };
      }
        
      if(!(unique_words.has(word))) {
        keywords_count[word].count = keywords_count[word].count + 1;
      }

      unique_words.add(word);

      keywords_count[word].frequency = keywords_count[word].frequency + 1;
    })
  });

  const data = Object.entries(keywords_count).map(([keyword, value]) => {
    return {
      name: keyword,
      count: value.count,
      frequency: value.frequency,
      proportion: tweetOjects !== undefined ? value.count / tweetOjects.length : 0
    };
  }).sort((a, b) => 
    // sort by count, then by frequency, then by name
    ((b.count - a.count) || (b.frequency - a.frequency) || (a.name.localeCompare(b.name)))
  ).slice(0, 10);

  return (
    <div className="vis-container">
      <VisHeader title={`Top 10 keywords`} subtitle={"Top 10 keywords"} />
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
            <YAxis dataKey='name' type="category" interval={0} fontSize={12} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar name="Number of tweets" dataKey="count" fill={ColorVar.blue} >
              {data.map((item) => (
                <>
                  <LabelList
                    dataKey="count"
                    position="right"
                    offset={5}
                    key={`cell-${item.name}`}
                  />
                  <Cell
                    fill={(item.name === filterOptions.keyword ? ColorVar.orange : ColorVar.blue)}
                    onClick={() => {
                      updateFilterOption("keyword", item.name);
                    }}
                    key={`cell-${item.name}`}
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

export default KeywordsCountBarChart;
