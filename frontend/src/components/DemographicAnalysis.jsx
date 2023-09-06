import React from 'react';
import VisHeader from './VisHeader';
import { Col, Row, Space } from 'antd';
import DATATYPES from '../constants/dataTypes';
import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip } from 'recharts';
import CircleProgressVis from './vis/CircleProgressVis';

const data = DATATYPES.analyticsBox;

export default function DemographicAnalysis() {
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        <Row>
          <Col span={12}>
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
                <Col span={4} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
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
          <Col span={1}></Col>
          <Col span={11} style={{ padding: 20 }}>
            {data.dataBoxRight.map((item, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: 'space-around',
                  alignItems: 'center',
                  border: '1px solid',
                  borderColor: item.colorChart,
                  borderRadius: 10,
                  padding: 20,
                  backgroundColor: item.bgColor,
                  color: item.textColor,
                  marginBottom: 20,
                }}
              >
                <CircleProgressVis
                  textColor={item.textColor}
                  bgColor={item.colorChart}
                  percent={((item.value / item.total) * 100).toFixed(0)}
                />
                <div>
                  <p style={{ fontSize: 16 }}>{item.title}</p>
                  <p style={{ fontSize: 26 }}>{item.value} tweets</p>
                </div>
              </div>
            ))}
          </Col>
        </Row>
      </div>
    </div>
  );
}
