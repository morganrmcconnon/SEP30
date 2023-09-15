import React, { useLayoutEffect } from 'react';
import { HiOutlineArrowCircleDown, HiOutlineArrowCircleUp } from 'react-icons/hi';
import { Divider, Space } from 'antd';
import dayjs from 'dayjs';

import DATATYPES from '../constants/dataTypes';
import VisHeader from '../grid_components/VisHeader';

const data = DATATYPES.top5Trends;

export default function TopTrends() {
  const [TopTrend, setTopTrend] = React.useState([]);
  const [listTrends, setListTrends] = React.useState([]);

  useLayoutEffect(() => {
    setTopTrend(data?.data.filter((item) => item?.topTrend));
    setListTrends(
      data?.data.filter((item) => !item?.topTrend).sort((a, b) => (a.status === 'up' ? -1 : b.status === 'up' ? 1 : 0)),
    );
  }, []);
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        {TopTrend && (
          <div
            style={{
              margin: 30,
              padding: 30,
              backgroundColor: '#d3f9d8',
              borderRadius: 10,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <div
              style={{
                width: 50,
                height: 50,
                backgroundColor: '#8ce99a',
                borderRadius: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <div style={{ width: 30, height: 30, backgroundColor: '#51cf66', borderRadius: '100%' }}></div>
            </div>
            <div style={{ marginLeft: 20 }}>
              <p>{TopTrend[0]?.title}</p>
              <p>{TopTrend[0]?.subTitle}</p>
            </div>
          </div>
        )}
        <div direction='vertical' style={{ margin: 30, marginTop: 0, height: 180, width: '90%', overflow: 'auto' }}>
          {listTrends.map((item, index) => (
            <>
              <div
                key={index}
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', margin: '10px 0' }}
              >
                <div>
                  <p>{item.title}</p>
                  <p className='text-data' style={{ marginTop: 3 }}>
                    {item.subTitle} | {dayjs(item.date).format('HH:mm:ss')}
                  </p>
                </div>
                <div style={{ paddingRight: 10 }}>
                  {item.status === 'up' ? (
                    <HiOutlineArrowCircleUp size={20} color='green' />
                  ) : (
                    <HiOutlineArrowCircleDown size={20} color='red' />
                  )}
                </div>
              </div>
              <Divider style={{ margin: 0 }} />
            </>
          ))}
        </div>
      </div>
    </div>
  );
}
