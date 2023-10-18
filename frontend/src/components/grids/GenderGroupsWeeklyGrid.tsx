import { Col, Row, Space } from 'antd';
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip } from 'recharts';
import { TooltipProps } from 'recharts';

import { ColorMap } from "../../constants/Colors"
import { timestampIntToShortDayMonth, timestampToDayTimestamp } from '../../utils/DateTimeFunctions';

import VisHeader from '../grid_components/VisHeader';
import { useDashboardFilteredContext } from '../../contexts/DashboardFilteredContext';


const legendMap: Record<string, any> = {
  female: { title: 'Female', dataKey: 'female', color: ColorMap.female.normal },
  male: { title: 'Male', dataKey: 'male', color: ColorMap.male.normal },
}



const CustomTooltip = ({ active, payload }: TooltipProps<number, string>) => {
  if (active && payload && payload.length) {
    const item = payload[0].payload;
    return (
      <div style={{ backgroundColor: 'white', padding: 8, border: '1px solid black' }}>
        <p className='text-data'>Date: {item.date_string}</p>
        {payload.sort((a, b) => ((b.value as number) - (a.value as number))).map((item, index) => {
          return (
            <p key={index} className='text-data' style={{ color: item.color }}>{legendMap[item.name!].title}: {item.value} users</p>
          );
        })}
      </div>
    );
  }

  return null;
};




export default function GenderGroupsWeekly() {
  const { tweetOjects } = useDashboardFilteredContext();

  const min_timestamp = Math.min(...tweetOjects.map((item) => parseInt(item.timestamp_ms, 10)));
  const max_timestamp = Math.max(...tweetOjects.map((item) => parseInt(item.timestamp_ms, 10)));

  const min_date_timestamp = timestampToDayTimestamp(min_timestamp);
  const max_date_timestamp = timestampToDayTimestamp(max_timestamp);

  const dateStart = min_date_timestamp ? timestampIntToShortDayMonth(min_date_timestamp) : '';
  const dateEnd = max_date_timestamp ? timestampIntToShortDayMonth(max_date_timestamp) : '';


  const date_counts: Record<number, {
    date_timestamp: number,
    date_string: string,
    female: number,
    male: number,
  }> = {};

  for (let i = min_date_timestamp; i <= max_date_timestamp; i += 86400000) {
    date_counts[i] = {
      date_string: timestampIntToShortDayMonth(i),
      date_timestamp: i,
      female: 0,
      male: 0,
    };
  }

  tweetOjects.forEach((tweet_object) => {
    const date_key = timestampToDayTimestamp(parseInt(tweet_object.timestamp_ms, 10));
    date_counts[date_key][tweet_object.user.gender] += 1;
  });
  
  const date_array = Object.values(date_counts).sort((a, b) => a.date_timestamp - b.date_timestamp);


  return (
    <div className='vis-container'>
      <VisHeader title='Mental Health Tweets by Gender' subtitle='Tweets count over time by Gender' />
      <div className='vis-svg-container'>
        <Row>
          <Col span={24}>

            <Row>
              <Col span={1} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p className='text-data' style={{ fontWeight: 'bold', transform: 'rotate(90deg)', margin: '10px 0 0 10px' }} >
                  {"Tweets"}
                </p>
              </Col>
              <Col span={22}>
                <ResponsiveContainer width='100%' height={250}>
                  <LineChart
                    data={date_array}
                    margin={{
                      top: 20,
                      bottom: 5,
                      left: 10,
                    }}
                  >
                    <Tooltip content={<CustomTooltip />} />
                    <ReferenceLine x={0} stroke='#000' style={{ height: 3 }} />
                    <ReferenceLine y={0} stroke='#000' style={{ height: 3 }} />
                    {Object.values(legendMap).map((item) => (
                      <Line dataKey={item.dataKey} stroke={item.color} />
                    ))}
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
              {Object.values(legendMap).map((item, index) => (
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
              ))}
            </Space>
          </Col>
        </Row>
      </div>
    </div>
  );
}