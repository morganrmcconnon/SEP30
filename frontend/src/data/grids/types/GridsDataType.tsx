

import { AgeGroupData, SentimentData } from '../../api/types/constants';


export type TopicRow = {
  date: number,
  topic: string,
  mentionTimes: number,
};

export type GridsDataType = {
  analyticsBox: {
    title: string,
    subTitle: string,
    dataChart: {
      totalData: string,
      totalDataChange: string,
      dateStart: string,
      dateEnd: string,
      LegendList: Array<
        { title: string, color: string }
      >,
      dataLineChart: Array<{
        total: string,
        color: string,
        data: Array<{
          user1: number,
          user2: number,
        }>
      }>
    },
    dataBoxRight: Array<{
      title: string,
      value: number,
      total: number,
      colorChart: string,
      bgColor: string,
      textColor: string,
    }>,
  },
  top5Trends: {
    title: string,
    subTitle: string,
    data: Array<{
      title: string,
      subTitle: string,
      year: string,
      date: number,
      status: string,
      topTrend: boolean,
    }>,
  },
  topicModelling: {
    title: string,
    subTitle: string,
    columns: Array<{}>,
    data: Array<TopicRow>,
  },
  sentimentAnalysis: {
    title: string,
    subTitle: string,
    values: SentimentData,
    data: Array<{
      value_key: keyof SentimentData,
      title: string,
      subTitle: string,
      value: number,
      color: string,
    }>,
  },
  agegroups: {
    title: string,
    subTitle: string,
    data: Array<{
      id: keyof AgeGroupData,
      name: string,
      percent: number,
      color: string,
    }>,
  },
  genders: {
    title: string,
    subTitle: string,
    data: {
      female: {
        present: number,
        color: string,
        activeList: Array<string>,
        sentiment: Record<string, number>,
      },
      male: {
        present: number,
        color: string,
        activeList: Array<string>,
        sentiment: Record<string, number>,
      },
    },
  },
  locations: {
    title: string,
    subTitle: string,
    locationHighLight: Array<string>,
    locationHighLightData: Array<number>,
    totalUser: number,
    data: Array<{
      name: string,
      value: number,
    }>,
  },
  knowledgeGraph: {
    title: string,
    subTitle: string,
    data: {
      nodes: Array<{
        id: string,
        group: number,
      }>,
      links: Array<{
        source: string,
        target: string,
        value: number,
      }>,
    }
  },
  keywordsDistribution: {
    title: string,
    subTitle: string,
    data: Array<{
      name: string,
      value: number,
    }>,
  },
  analyticsAgeBox: {
    title: string,
    subTitle: string,
    dataChart: {
      totalData: string,
      dateStart: number,
      dateEnd: number,
      LegendList: Array<{ title: string, color: string }>,
      dataLineChart: [
        {
          total: string,
          color: string,
          data: Array<{
            'Under 18': number,
            '19 - 29': number,
            '30 - 39': number,
            '40 and above': number,
          }>
        },
      ],
    },
  },
  analyticsSentimentBox: {
    title: string,
    subTitle: string,
    dataChart: {
      totalData: string,
      dateStart: number,
      dateEnd: number,
      LegendList: Array<{ title: string, color: string }>,
      dataLineChart: [
        {
          data: Array<{
            Positive: number,
            Negative: number,
            Neutral: number,
          }>
        },
      ],
    },
  },
  analyticsGenderBox: {
    title: string,
    subTitle: string,
    dataChart: {
      dateStart: number,
      dateEnd: number,
      LegendList: Array<{ title: string, color: string }>
      dataLineChart: [
        {
          data: Array<{
            Female: number,
            Male: number,
          }>,
        },
      ],
    },
  },
};


