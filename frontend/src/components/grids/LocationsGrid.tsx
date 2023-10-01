import { Col, Row, Space } from 'antd';
import { ComposableMap, Geographies, Geography, Graticule, Sphere, ZoomableGroup } from 'react-simple-maps';
// import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
// import { PatternLines } from '@vx/pattern';
// import { AiOutlineReload } from 'react-icons/ai';

import VisHeader from '../grid_components/VisHeader';
import ProgressBar from '../grid_components/ProgressBar';
import { useSearchContext } from '../../contexts/SearchContext';

const geoUrl = '/features.json';

const colorArray = [
  "#AEDFF7",
  "#7DBDE8",
  "#4C96D9",
  "#2F6DB7",
  "#1A478E"
];

export default function LocationsGrid() {
  const { dashboardData } = useSearchContext();

  const data = dashboardData.locations;
  // Initialize max to a minimum possible value
  let maxValue = -Infinity;

  // Iterate through the object's values
  data?.data.forEach(function (element) {

    if (element.name != 'UNCATEGORISED' && element.value > maxValue) {
      maxValue = element.value;
    }
  })
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
					color={colorArray[Math.min(4, Math.round(item.value * 4 / maxValue))]}
                    rounded={10}
                    percent={((item.value / maxValue) * 100).toFixed(0)}
                  />
                </div>
              ))}


            </Space>
          </Col>
          <Col span={18} style={{ overflow: 'hidden' }}>
            <MapChart Highlighted={data?.locationHighLight} mymaxvalue={maxValue} />
          </Col>
        </Row>
      </div>
    </div>
  );
}

const MapChart = ({ Highlighted, mymaxvalue }: { Highlighted: string[], mymaxvalue: number }) => {
  const { updateFilterOption, dashboardData } = useSearchContext();
  return (
    <div style={{ width: '85%', position: 'relative', left: '42%', transform: 'translateX(-40%)', top: '-15%' }}>
      <ComposableMap projection='geoEqualEarth'>
        <ZoomableGroup center={[0, 0]}>
          <Sphere stroke='#DDD' id={''} fill={'#FFF'} strokeWidth={0} />
          <Graticule stroke='#DDD' />
          <Geographies geography={geoUrl} stroke='#FFF' strokeWidth={0.5}>
            {({ geographies }) =>
              geographies.map((geo) => {
                const isHighlighted = Highlighted.indexOf(geo.id) !== -1;
                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    //replace 0 by 
                    fill={isHighlighted ? colorArray[Math.round(dashboardData.locations?.locationHighLightData[Highlighted.indexOf(geo.id)] * 4 / mymaxvalue)] : '#F6F0E9'}
                    onClick={() => { isHighlighted ? updateFilterOption('location', geo.id) : ""; }}
                    // fill={isHighlighted ? "url('#lines')" : '#F6F0E9'}
                    // onClick={() => console.log(geo.properties.name)}
                  />
                );
              })
            }
          </Geographies>
        </ZoomableGroup>

      </ComposableMap>
    </div>
  );
};
