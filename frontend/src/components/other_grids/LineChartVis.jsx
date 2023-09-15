import { ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis } from 'recharts';

import VisHeader from '../grid_components/VisHeader';
import ColorVar from '../../constants/ColorVar';

const data = [
  { name: 'A', uv: 400 },
  { name: 'B', uv: 300 },
  { name: 'C', uv: 600 },
  { name: 'D', uv: 650 },
  { name: 'E', uv: 300 },
];

const LineChartVis = () => {
  return (
    <div className='vis-container'>
      <VisHeader title='Line Chart' subtitle='Line Subtitle' />
      <div className='vis-svg-container'>
        <ResponsiveContainer width='95%' height={400}>
          <LineChart data={data}>
            <Line type='natural' dataKey='uv' stroke={ColorVar.blue} />
            <CartesianGrid stroke='#868e96' strokeDasharray='5 5' />
            <XAxis dataKey='name' />
            <YAxis />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default LineChartVis;
