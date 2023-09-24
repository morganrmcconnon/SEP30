import { Col, Row, Space } from 'antd';
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip } from 'recharts';

import VisHeader from '../grid_components/VisHeader';
import { useSearchContext } from '../../contexts/SearchContext';


export default function AgeGroupsWeekly() {
  const { dashboardData } = useSearchContext();
  const data = dashboardData.analyticsBox;

  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        <Row>
          <Col span={24}>
            <Row>
              <Col
                span={4}
                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}
              >
                <p className='text-data' style={{ fontWeight: 'bold' }}>
                  Data
                </p>
              </Col>
              <Col span={20}>
                <p style={{ fontWeight: 'bold', fontSize: 25, margin: '10px 0 0 30px' }}>
                  {data?.dataChart.totalData} <span className='text-data'>{data?.dataChart.totalDataChange}</span>
                </p>
              </Col>
            </Row>
            {data.dataChart.dataLineChart.map((item, index) => (
              <Row key={index}>
                <Col span={2} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <p className='text-data' style={{ fontWeight: 'bold' }}>
                    {item?.total}
                  </p>
                </Col>
                <Col span={20}>
                  <ResponsiveContainer width='100%' height={80}>
                    <LineChart
                      data={item?.data}
                      margin={{
                        top: 20,
                        bottom: 5,
                        left: 10,
                      }}
                    >
                      <Tooltip />
                      <ReferenceLine y={5000} stroke='#000' style={{ height: 3 }} />
                      <Line dataKey='user2' stroke={item?.color} />
                      <Line dataKey='user1' stroke={item?.color} strokeDasharray='3 4 5 2' />
                    </LineChart>
                  </ResponsiveContainer>
                  {data.dataChart.dataLineChart.length === index + 1 && (
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span className='text-data' style={{ fontWeight: 'bold' }}>
                        {data?.dataChart.dateStart}
                      </span>
                      <span className='text-data' style={{ fontWeight: 'bold' }}>
                        {data?.dataChart.dateEnd}
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
                      borderColor: item.color,
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
