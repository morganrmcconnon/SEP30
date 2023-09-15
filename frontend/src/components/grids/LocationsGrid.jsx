import React from 'react';
import { Col, Row, Space } from 'antd';
import { ComposableMap, Geographies, Geography, Graticule, Sphere } from 'react-simple-maps';
// import { PatternLines } from '@vx/pattern';

import VisHeader from '../grid_components/VisHeader';
import ProgressBar from '../grid_components/ProgressBar';
import DATATYPES from '../../constants/dataTypes';
import { useSearchContext } from '../../contexts/SearchContext';

const geoUrl = '/features.json';

export default function LocationsGrid() {
  const { search, updateSearch, dashboardData } = useSearchContext();
  const data = dashboardData.locations;
  return (
    <div className='vis-container'>
      <VisHeader title={data?.title} subtitle={data?.subTitle} />
      <div className='vis-svg-container'>
        <Row style={{ margin: 30 }}>
          <Col span={6}>
            <Space direction='vertical' style={{ width: '100%' }}>
              {data?.data.map((item) => (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
                    <p>{item.name}</p>
                    <p className='text-data'>{item.value} Users</p>
                  </div>
                  <ProgressBar
                    width='100%'
                    height={13}
                    color='#339aef'
                    rounded={10}
                    percent={((item.value / data.totalUser) * 100).toFixed(0)}
                  />
                </div>
              ))}
            </Space>
          </Col>
          <Col span={16} style={{ overflow: 'hidden' }}>
            <MapChart Highlighted={data?.locationHighLight} />
          </Col>
        </Row>
      </div>
    </div>
  );
}

const MapChart = ({ Highlighted }) => {
  const { search, updateSearch, dashboardData } = useSearchContext();
  return (
    <div style={{ width: '80%', position: 'relative', left: '50%', transform: 'translateX(-40%)', top: '-10%' }}>
      <ComposableMap projection='geoEqualEarth'>
        {/* <PatternLines
          id='lines'
          height={6}
          width={6}
          stroke='#776865'
          strokeWidth={1}
          background='#F6F0E9'
          orientation={['diagonal']}
        /> */}
        <Sphere stroke='#DDD' />
        <Graticule stroke='#DDD' />
        <Geographies geography={geoUrl} stroke='#FFF' strokeWidth={0.5}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const isHighlighted = Highlighted.indexOf(geo.id) !== -1;
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={isHighlighted ? "#339AF0" : '#F6F0E9'}
                  onClick={() => {
                    updateSearch({ ...search, location: geo.properties.name });
                  }
                  }
                // fill={isHighlighted ? "url('#lines')" : '#F6F0E9'}
                // onClick={() => console.log(geo.properties.name)}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>
    </div>
  );
};
