import { Col, Row, Space } from 'antd';
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip } from 'recharts';

import VisHeader from '../grid_components/VisHeader';
import { useSearchContext } from '../../contexts/SearchContext';


export default function GenderGroupsWeekly() {
  const { dashboardData } = useSearchContext();
  const data = dashboardData.analyticsGenderBox;
	const color = ["#339AF0", "#51CF66", "#FFFFFF"];
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        <Row>
          <Col span={24}>
            
            {data.dataChart.dataLineChart.map((item, index) => (
              <Row key={index} >
                <Col span={1} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <p  className='text-data' style={{ fontWeight: 'bold', transform: 'rotate(90deg)' , margin: '10px 0 0 10px' }} >
					  {"Tweets"}
                  </p>
                </Col>
                <Col span={22}>
                  <ResponsiveContainer width='100%' height={250}>
                    <LineChart
                      data={item?.data}
                      margin={{
                        top: 20,
                        bottom: 5,
                        left: 10,
                      }}
                    >
                      <Tooltip />
					  <ReferenceLine x={0} stroke='#000' style={{ height: 3 }} />
                      <ReferenceLine y={0} stroke='#000' style={{ height: 3 }} />
                      <Line dataKey='Female' stroke={color[0]} />
					  <Line dataKey='Male' stroke={color[1]} />

                    </LineChart>
                  </ResponsiveContainer>
                  {data.dataChart.dataLineChart.length === index + 1 && (
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span className='text-data' style={{ fontWeight: 'bold' }}>
    {data?.dataChart.dateStart ? new Date(data.dataChart.dateStart * 1000).toLocaleDateString(undefined, { month: 'short',day: 'numeric' }) : ''}
                      </span>
                      <span className='text-data' style={{ fontWeight: 'bold' }}>
    {data?.dataChart.dateEnd ? new Date(data.dataChart.dateEnd * 1000).toLocaleDateString(undefined, { month: 'short',day: 'numeric' }) : ''}
                      </span>
                    </div>
                  )}
                </Col>
              </Row>
            ))}
            <Space size='large' style={{ marginLeft: 30, marginTop: 20 }}>
              {data?.dataChart.LegendList.map((item, index) => (
                <div style={{ display: 'flex', alignItems: 'center' }} key={index}>
                  <div
                    style={{
                      width: 6,
                      height: 6,
                      border: '3px solid',
                      borderRadius: '100%',
                      marginRight: 6,
                      borderColor: item?.color,
                    }}
                  />
                  <span className='text-data'>{item?.title}</span>
                </div>
              ))}
            </Space>
          </Col>
        </Row>
      </div>
    </div>
  );
}
