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
      <div style={{ backgroundColor: '#fff', padding: 8, border: '1px solid black' }} className="text-black-white">
        <p>{`"${label}"`}</p>
        <p>{item.count} tweets ({Math.round(item.proportion * 10000) / 100}%)</p>
      </div>
    );
  }

  return null;
};

const TopicsCountBarChart = () => {
  const { filterOptions, updateFilterOption, tweetOjects } = useDashboardFilteredContext();

  const topics_count: Record<string, number> = {};

  tweetOjects?.forEach((tweet) => {
    tweet.topic_lda.related_topics.cosine_similarity.forEach((topic) => {
      if (topic !== undefined) {
        if (topics_count[topic] === undefined) {
          topics_count[topic] = 1;
        } else {
          topics_count[topic] += 1;
        }
      }
    }
    )
  });

  const data = Object.entries(topics_count).map(([topic, topic_count]) => {
    return { name: topic, value: topic_count, count: topic_count, proportion: (tweetOjects !== undefined ? topic_count / tweetOjects.length : 0) };
  }).sort((a, b) => b.value - a.value).slice(0, 10);

  return (
    <div className="vis-container">
      <VisHeader title={"Top 10 related topics"} subtitle={"Top 10 related topics"} />
      <div className="vis-svg-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={280}
            data={data}
            layout="vertical"
            margin={{
              top: 5,
              right: 50,
              left: 50,
              bottom: 5,
            }}
            barGap={100}
          >
            <CartesianGrid  strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey='name' type="category" interval={0} fontSize={12} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <ReferenceLine y={0} stroke="#000" />
            <Bar name="Number of tweets" dataKey="value" fill={ColorVar.blue} >
              {data.map((item) => (
                <>
                  <LabelList
                    dataKey="count"
                    position="right"
                    offset={5}
                  />
                  <Cell
                    fill={(item.name === filterOptions.topic ? ColorVar.red : ColorVar.blue)}
                    onClick={() => {
                      updateFilterOption("topic", item.name);
                    }}
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

export default TopicsCountBarChart;
