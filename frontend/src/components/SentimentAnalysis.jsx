import React from 'react';
import VisHeader from './VisHeader';
import DATATYPES from '../constants/dataTypes';
import { FaStar } from 'react-icons/fa';
import { Divider } from 'antd';

const data = DATATYPES.sentimentAnalysis;

export default function SentimentAnalysis() {
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container' style={{ height: 350, overflow: 'auto' }}>
        {data?.data.map((item, index) => (
          <>
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '5px 20px',
              }}
            >
              <div style={{ margin: '5px 0' }}>
                <p style={{ fontSize: 18 }}>{item.title}</p>
                <p className='text-data'>{item.subTitle}</p>
              </div>
              <div style={{ display: 'flex' }}>
                <FaStar color='yellow' />
                <p style={{ marginLeft: 10 }}>{item.star}</p>
              </div>
            </div>
            <Divider style={{ margin: '10px 0' }} />
          </>
        ))}
      </div>
    </div>
  );
}
