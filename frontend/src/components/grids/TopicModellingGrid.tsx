import { Table } from 'antd';

import VisHeader from '../grid_components/VisHeader';
import { useSearchContext } from '../../contexts/SearchContext';


export default function TopicModelling() {
  const { updateFilterOption, dashboardData } = useSearchContext();
  const data = dashboardData.topicModelling;

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
          onRow={(record) => {
            return {
              onClick: () => {
                updateFilterOption('topic', record.topic);
              },
            };
          }
          }
        />
      </div>
    </div>
  );
}
