import React from 'react';
import VisHeader from './VisHeader';
import DATATYPES from '../constants/dataTypes';
import { Table } from 'antd';

const data = DATATYPES.topicModelling;

export default function TopicModelling() {
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        <Table
          columns={data?.columns}
          dataSource={data?.data}
          pagination={false}
          scroll={{
            y: 300,
          }}
        />
      </div>
    </div>
  );
}
