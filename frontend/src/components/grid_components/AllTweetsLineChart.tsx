import { Col, Row, Space } from 'antd';
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip } from 'recharts';
import { TooltipProps } from 'recharts';

import { ColorVar } from "../../constants/Colors"
import { timestampIntToShortDayMonth, timestampToDayTimestamp } from '../../utils/DateTimeFunctions';

import { useDashboardFilteredContext } from '../../contexts/DashboardFilteredContext';


const legendMap: Record<string, any> = {
  count: { title: 'Mental health related tweets count', dataKey: 'count', color: ColorVar.blue },
  displayed: { title: 'Visualised tweets count', dataKey: 'displayed', color: ColorVar.orange },
}

const CustomTooltip = ({ active, payload }: TooltipProps<number, string>) => {
  if (active && payload && payload.length) {
    const item = payload[0].payload;
    return (
      <div style={{ backgroundColor: 'white', padding: 8, border: '1px solid black' }}>
        <p className='text-data' style={{ color: 'black' }}>Date: {item.date_string}</p>
        {payload.sort((a, b) => ((b.value as number) - (a.value as number))).map((item, index) => {
          return (
            <p key={index} className='text-data' style={{ color: item.color }}>{item.value} tweets</p>
          );
        })}
      </div>
    );
  }

  return null;
};


const AllTweetsLineChart: React.FC<{
  height: number;
}> = (props) => {
  const { tweetOjects, backendData, filterOptions, updateFilterOption } = useDashboardFilteredContext();

  const original_tweetOjects = backendData?.tweet_objects || [];

  const min_timestamp = Math.min(...original_tweetOjects.map((item) => parseInt(item.timestamp_ms, 10)));
  const max_timestamp = Math.max(...original_tweetOjects.map((item) => parseInt(item.timestamp_ms, 10)));

  const min_date_timestamp = timestampToDayTimestamp(min_timestamp);
  const max_date_timestamp = timestampToDayTimestamp(max_timestamp);

  const dateStart = min_date_timestamp ? timestampIntToShortDayMonth(min_date_timestamp) : '';
  const dateEnd = max_date_timestamp ? timestampIntToShortDayMonth(max_date_timestamp) : '';


  const date_counts: Record<number, {
    date_timestamp: number,
    date_string: string,
    count: number,
    displayed: number,
  }> = {};

  for (let i = min_date_timestamp; i <= max_date_timestamp; i += 86400000) {
    date_counts[i] = {
      date_string: timestampIntToShortDayMonth(i),
      date_timestamp: i,
      count: original_tweetOjects.filter((item) => timestampToDayTimestamp(parseInt(item.timestamp_ms, 10)) === i).length || 0,
      displayed: tweetOjects.filter((item) => timestampToDayTimestamp(parseInt(item.timestamp_ms, 10)) === i).length,
    };
  }

  const date_array = Object.values(date_counts).sort((a, b) => a.date_timestamp - b.date_timestamp);

  let index = 0;
  let item = legendMap.count;

  if (Object.values(filterOptions).some((item) => item !== null)) {
    item = legendMap.displayed;
    index = 1;
  }

  return (
    <>
      <Row>
        <Col span={1} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <p className='text-data' style={{ fontWeight: 'bold', transform: 'rotate(90deg)', margin: '10px 0 0 10px' }} >
            {"Tweets"}
          </p>
        </Col>
        <Col span={22}>
          <ResponsiveContainer width='100%' height={props.height}>
            <LineChart
              data={date_array}
              margin={{
                top: 20,
                bottom: 5,
                left: 10,
              }}
              onClick={(event) => {
                if(event.activePayload) {
                  updateFilterOption('date', event.activePayload[0].payload.date_string);
                }
              }}
            >
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine x={0} stroke='#000' style={{ height: 3 }} />
              <ReferenceLine y={0} stroke='#000' style={{ height: 3 }} />
              <Line dataKey={item.dataKey} stroke={item.color} />
            </LineChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span className='text-data' style={{ fontWeight: 'bold' }}>
              {dateStart}
            </span>
            <span className='text-data' style={{ fontWeight: 'bold' }}>
              {dateEnd}
            </span>
          </div>
        </Col>
      </Row>
      <Space size='large' style={{ marginLeft: 30, marginTop: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center' }} key={index}>
          <div
            style={{
              width: 6,
              height: 6,
              border: '3px solid',
              borderRadius: '100%',
              marginRight: 6,
              borderColor: item.color,
            }}
          />
          <span className='text-data'>{item.title}</span>
        </div>
      </Space>
    </>
  );
}


export default AllTweetsLineChart;