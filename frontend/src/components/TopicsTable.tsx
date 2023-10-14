import { Table } from 'antd';
import { BsArrowRight } from 'react-icons/bs';

// import { ColorVar } from '../../../constants/Colors';
// import { GridsDataType } from '../types/GridsDataType';
import VisHeader from '../grid_components/VisHeader';
import { useDashboardFilteredContext } from '../../contexts/DashboardFilteredContext';

const columns = [
  {
    title: 'Topic',
    dataIndex: 'topic',
    key: 'topic',
    sorter: (a: { topic: string }, b: { topic: string }) => a.topic.localeCompare(b.topic),
  },
  {
    title: 'Count',
    dataIndex: 'count',
    key: 'count',
    render: (count: number) => (
      <div className='text-black-white' style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <p>{count} {count == 1 ? 'tweet' : 'tweets'}</p>
      </div>
    ),
    sorter: (a: { count: number }, b: { count: number }) => a.count - b.count,
  },
  {
    title: 'Proportion',
    dataIndex: 'proportion',
    key: 'proportion',
    render: (proportion: number) => (
      <div className='text-black-white' style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <p>{Math.round(proportion * 10000) / 100}%</p>
        <BsArrowRight />
      </div>
    ),
    sorter: (a: { proportion: number }, b: { proportion: number }) => a.proportion - b.proportion,
  },
];

export default function TopicsTable() {
  const { updateFilterOption: updateFilterOptions, tweetOjects } = useDashboardFilteredContext();

  const topics_count: Record<string, number> = {};

  tweetOjects?.forEach((tweet) => {
    tweet.topic_lda.related_topics.cosine_similarity.forEach((topic) => {
      if (topic !== undefined) {
        if (topics_count[topic] === undefined) {
          topics_count[topic] = 1;
        } else {
          topics_count[topic] += 1;
        }
      }
    }
    )
  });


  const data = Object.entries(topics_count).map(([topic, topic_count]) => {
    return { topic: topic, count: topic_count, proportion: (tweetOjects !== undefined ? topic_count / tweetOjects.length : 0) };
  });


  return (
    <div className='vis-container'>
      <VisHeader title={'Topics'} subtitle={'List of related topics'} />
      <div className='vis-svg-container'>
        <Table
          columns={columns}
          dataSource={data}
          pagination={false}
          scroll={{
            y: 300,
          }}
          onRow={(record) => {
            return {
              onClick: () => {
                updateFilterOptions('topic', record.topic);
              },
            };
          }
          }
        />
      </div>
    </div>
  );
}
