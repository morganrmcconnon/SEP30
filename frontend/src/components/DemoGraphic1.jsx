import React from 'react';
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import VisHeader from './VisHeader';
import DATATYPES from '../constants/dataTypes';
import { Col, Row } from 'antd';

const data = DATATYPES.demoGraphic1;

export default function DemoGraphic1() {
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        <ResponsiveContainer width='100%' height={260}>
          <PieChart>
            <Pie dataKey='percent' data={data.data} cy={130} innerRadius={60} outerRadius={100} fill='#82ca9d'>
              {data.data.map((item, index) => (
                <Cell key={`cell-${index}`} fill={item.color} strokeWidth={10} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
        <Row style={{ margin: '20px' }}>
          {data.data.map((item, index) => (
            <Col
              span={12}
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 18 }}
              key={index}
            >
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
              <p>
                {item?.name} ({item?.percent}%)
              </p>
            </Col>
          ))}
        </Row>
      </div>
    </div>
  );
}
