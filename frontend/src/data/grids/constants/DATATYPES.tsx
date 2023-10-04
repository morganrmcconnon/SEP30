import { BsArrowRight } from 'react-icons/bs';
import { ColorVar } from '../../../constants/Colors';
import { GridsDataType } from '../types/GridsDataType';

export const DATATYPES: GridsDataType = {
  analyticsBox: {
    title: 'Real-time Analysis',
    subTitle: 'Real-time Analysis results',
    dataChart: {
      totalData: '1.5M',
      totalDataChange: '-0.8%',
      dateStart: 'Dec19',
      dateEnd: 'Dec25',
      LegendList: [
        { title: 'Total', color: ColorVar.blue },
        { title: 'CTG1', color: ColorVar.green },
        { title: 'CTG2', color: ColorVar.orange },
      ],
      dataLineChart: [
        {
          total: '1.5M',
          color: ColorVar.blue,
          data: [
            {
              user1: 4000,
              user2: 2400,
            },
            {
              user1: 3000,
              user2: 1398,
            },
            {
              user1: 2000,
              user2: 9800,
            },
            {
              user1: 2780,
              user2: 3908,
            },
            {
              user1: 1890,
              user2: 4800,
            },
            {
              user1: 2390,
              user2: 3800,
            },
            {
              user1: 3490,
              user2: 4300,
            },
          ],
        },
        {
          total: '1.1M',
          color: ColorVar.green,
          data: [
            {
              user1: 4000,
              user2: 2400,
            },
            {
              user1: 3000,
              user2: 1398,
            },
            {
              user1: 2000,
              user2: 9800,
            },
            {
              user1: 2780,
              user2: 3908,
            },
            {
              user1: 1890,
              user2: 4800,
            },
            {
              user1: 2390,
              user2: 3800,
            },
            {
              user1: 3490,
              user2: 4300,
            },
          ],
        },
        {
          total: '608K',
          color: ColorVar.orange,
          data: [
            {
              user1: 4000,
              user2: 2400,
            },
            {
              user1: 3000,
              user2: 1398,
            },
            {
              user1: 2000,
              user2: 9800,
            },
            {
              user1: 2780,
              user2: 3908,
            },
            {
              user1: 1890,
              user2: 4800,
            },
            {
              user1: 2390,
              user2: 3800,
            },
            {
              user1: 3490,
              user2: 4300,
            },
          ],
        },
      ],
    },
    dataBoxRight: [
      {
        title: 'Related Tweets',
        value: 1602,
        total: 2000,
        colorChart: 'white',
        bgColor: ColorVar.blue,
        textColor: 'white'
      },
      {
        title: 'Displaying',
        value: 1255,
        total: 2000,
        colorChart: ColorVar.orange,
        bgColor: 'white',
        textColor: '#000',
      },
    ],
  },
  top5Trends: {
    title: 'Top 5 Trends',
    subTitle: 'Update by',
    data: [
      { title: 'Trend 1', subTitle: 'Subtitle', year: '2020', date: Date.now(), status: 'up', topTrend: true },
      { title: 'Trend 2', subTitle: 'Subtitle', year: '2020', date: Date.now(), status: 'up', topTrend: false },
      { title: 'Trend 3', subTitle: 'Subtitle', year: '2020', date: Date.now(), status: 'up', topTrend: false },
      { title: 'Trend 4', subTitle: 'Subtitle', year: '2020', date: Date.now(), status: 'down', topTrend: false },
      { title: 'Trend 5', subTitle: 'Subtitle', year: '2020', date: Date.now(), status: 'down', topTrend: false },
      { title: 'Trend 6', subTitle: 'Subtitle', year: '2020', date: Date.now(), status: 'down', topTrend: false },
    ],
  },
  topicModelling: {
    title: 'Topic modelling',
    subTitle: 'Topic modelling result',
    columns: [
      // {
      //   title: 'Date',
      //   dataIndex: 'date',
      //   key: 'date',
      //   render: (date) => (
      //     <div>
      //       <p>{dayjs(date).format('YYYY/MM/DD')}</p>
      //       <p>{dayjs(date).format('HH:mm')}</p>
      //     </div>
      //   ),
      // },
      {
        title: 'Topic',
        dataIndex: 'topic',
        key: 'topic',
        sorter: (a: { topic: string }, b: { topic: string }) => a.topic.localeCompare(b.topic),
      },
      {
        title: 'Number of tweets',
        dataIndex: 'mentionTimes',
        key: 'mentionTimes',
        render: (mentionTimes: number) => (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <p>{mentionTimes}</p>
            <BsArrowRight />
          </div>
        ),
        sorter: (a: { mentionTimes: number }, b: { mentionTimes: number }) => a.mentionTimes - b.mentionTimes,
      },
    ],
    data: [
      { date: Date.now(), topic: 'Topic 1', mentionTimes: 1000 },
      { date: Date.now(), topic: 'Topic 2', mentionTimes: 900 },
      { date: Date.now(), topic: 'Topic 3', mentionTimes: 800 },
      { date: Date.now(), topic: 'Topic 4', mentionTimes: 700 },
      { date: Date.now(), topic: 'Topic 5', mentionTimes: 600 },
      { date: Date.now(), topic: 'Topic 6', mentionTimes: 500 },
      { date: Date.now(), topic: 'Topic 7', mentionTimes: 300 },
      { date: Date.now(), topic: 'Topic 8', mentionTimes: 200 },
      { date: Date.now(), topic: 'Topic 9', mentionTimes: 100 },
    ],
  },
  sentimentAnalysis: {
    title: 'Sentiment Analysis',
    subTitle: 'Total tweets per sentiment',
    values: {
      positive: 100,
      negative: 50,
      neutral: 50,
    },
    data: [
      { value_key: 'positive', title: 'Positive Tweets', subTitle: 'Number of positive tweets', value: 199, color: ColorVar.green },
      { value_key: 'neutral', title: 'Neutral Tweets', subTitle: 'Number of neutral tweets', value: 50, color: ColorVar.blue },
      { value_key: 'negative', title: 'Negative Tweets', subTitle: 'Number of negative tweets', value: 100, color: ColorVar.orange },
    ],
  },
  agegroups: {
    title: 'Demographic Analysis - Age Groups',
    subTitle: 'Age Groups percentage',
    data: [
      { id: '<=18', name: 'Under 18', percent: 18, color: ColorVar.blue },
      { id: '19-29', name: '19 - 29', percent: 40, color: '#50cc65' },
      { id: '30-39', name: '30 - 39', percent: 15, color: ColorVar.orange },
      { id: '>=40', name: '40 and above', percent: 15, color: ColorVar.red },
    ],
  },
  genders: {
    title: 'Demographic Analysis - Genders',
    subTitle: 'Demographic Analysis - Genders',
    data: {
      female: {
        present: 60,
        color: ColorVar.lightred,
        activeList: ['1', '2', '3', '4'],
        sentiment: {
          positive: 0,
          neutral: 0,
          negative: 0,
        },
      },
      male: {
        present: 40,
        color: '#d0ebff',
        activeList: ['5', '6', '7', '8'],
        sentiment: {
          positive: 0,
          neutral: 0,
          negative: 0,
        },
      },
    },
  },
  locations: {
    title: 'Demographic Analysis - Location',
    subTitle: 'Demographic Analysis - Location',
    locationHighLight: [
      'DEU', // Germany
      'FRA', // France
      'ITA', // Italy
      'ESP', // Spain
      'GBR', // United Kingdom
      'GRC', // Greece
      'PRT', // Portugal
      'NLD', // Netherlands
      'BEL', // Belgium
      'AUT', // Austria
      'CHE', // Switzerland
      'SWE', // Sweden
      'NOR', // Norway
      'DNK', // Denmark
      'FIN', // Finland
      'POL', // Poland
      'RUS', // Russia
      'UKR', // Ukraine
      'CZE', // Czech Republic
      'SVK', // Slovakia
      'HUN', // Hungary
      'AFG', // Afghanistan
      'ARM', // Armenia
      'AZE', // Azerbaijan
      'BHR', // Bahrain
      'BGD', // Bangladesh
      'BTN', // Bhutan
      'BRN', // Brunei
      'KHM', // Cambodia
      'CHN', // China
      'CYP', // Cyprus
      'GEO', // Georgia
      'IND', // India
      'IDN', // Indonesia
      'IRN', // Iran
      'IRQ', // Iraq
      'ISR', // Israel
      'JPN', // Japan
      'JOR', // Jordan
      'KAZ', // Kazakhstan
      'KGZ', // Kyrgyzstan
      'KWT', // Kuwait
      'LAO', // Laos
      'LBN', // Lebanon
      'MYS', // Malaysia
      'MDV', // Maldives
      'MNG', // Mongolia
      'MMR', // Myanmar (Burma)
      'NPL', // Nepal
      'OMN', // Oman
      'PAK', // Pakistan
      'PHL', // Philippines
      'QAT', // Qatar
      'SAU', // Saudi Arabia
      'SGP', // Singapore
      'KOR', // South Korea
      'LKA', // Sri Lanka
      'SYR', // Syria
      'TWN', // Taiwan
      'TJK', // Tajikistan
      'THA', // Thailand
      'TLS', // Timor-Leste (East Timor)
      'TUR', // Turkey
      'TKM', // Turkmenistan
      'ARE', // United Arab Emirates
      'UZB', // Uzbekistan
      'VNM', // Vietnam
      'YEM', // Yemen
      'DZA', // Algeria
      'AGO', // Angola
      'BEN', // Benin
      'BWA', // Botswana
      'BFA', // Burkina Faso
      'BDI', // Burundi
      'CMR', // Cameroon
      'CPV', // Cape Verde
      'CAF', // Central African Republic
      'TCD', // Chad
      'COM', // Comoros
      'COD', // Democratic Republic of the Congo
      'DJI', // Djibouti
      'EGY', // Egypt
      'GNQ', // Equatorial Guinea
      'ERI', // Eritrea
      'SWZ', // Eswatini (formerly Swaziland)
      'ETH', // Ethiopia
      'GAB', // Gabon
      'GMB', // Gambia
      'GHA', // Ghana
      'GIN', // Guinea
      'GNB', // Guinea-Bissau
      'CIV', // Ivory Coast
      'KEN', // Kenya
      'LSO', // Lesotho
      'LBR', // Liberia
      'LBY', // Libya
      'MDG', // Madagascar
      'MWI', // Malawi
      'MLI', // Mali
      'MRT', // Mauritania
      'MUS', // Mauritius
      'MAR', // Morocco
      'MOZ', // Mozambique
      'NAM', // Namibia
      'NER', // Niger
      'NGA', // Nigeria
      'RWA', // Rwanda
      'STP', // Sao Tome and Principe
      'SEN', // Senegal
      'SYC', // Seychelles
      'SLE', // Sierra Leone
      'SOM', // Somalia
      'ZAF', // South Africa
      'SSD', // South Sudan
      'SDN', // Sudan
      'TZA', // Tanzania
      'TGO', // Togo
      'TUN', // Tunisia
      'UGA', // Uganda
      'ZMB', // Zambia
      'ZWE', // Zimbabwe
      'AUS', // Australia
      'USA', // United States of America
    ],
    locationHighLightData: [
      1, // Germany
      1, // France
      1, // Italy
      1, // Spain
      1, // United Kingdom
      1, // Greece
      1, // Portugal
      1, // Netherlands
      1, // Belgium
      1, // Austria
      1, // Switzerland
      1, // Sweden
      1, // Norway
      1, // Denmark
      1, // Finland
      1, // Poland
      1, // Russia
      1, // Ukraine
      1, // Czech Republic
      1, // Slovakia
      1, // Hungary
      1, // Afghanistan
      1, // Armenia
      1, // Azerbaijan
      1, // Bahrain
      1, // Bangladesh
      1, // Bhutan
      1, // Brunei
      1, // Cambodia
      1, // China
      1, // Cyprus
      1, // Georgia
      1, // India
      1, // Indonesia
      1, // Iran
      1, // Iraq
      1, // Israel
      1, // Japan
      1, // Jordan
      1, // Kazakhstan
      1, // Kyrgyzstan
      1, // Kuwait
      1, // Laos
      1, // Lebanon
      1, // Malaysia
      1, // Maldives
      1, // Mongolia
      1, // Myanmar (Burma)
      1, // Nepal
      1, // Oman
      1, // Pakistan
      1, // Philippines
      1, // Qatar
      1, // Saudi Arabia
      1, // Singapore
      1, // South Korea
      1, // Sri Lanka
      1, // Syria
      1, // Taiwan
      1, // Tajikistan
      1, // Thailand
      1, // Timor-Leste (East Timor)
      1, // Turkey
      1, // Turkmenistan
      1, // United Arab Emirates
      1, // Uzbekistan
      1, // Vietnam
      1, // Yemen
      1, // Algeria
      1, // Angola
      1, // Benin
      1, // Botswana
      1, // Burkina Faso
      1, // Burundi
      1, // Cameroon
      1, // Cape Verde
      1, // Central African Republic
      1, // Chad
      1, // Comoros
      1, // Democratic Republic of the Congo
      1, // Djibouti
      1, // Egypt
      1, // Equatorial Guinea
      1, // Eritrea
      1, // Eswatini (formerly Swaziland)
      1, // Ethiopia
      1, // Gabon
      1, // Gambia
      1, // Ghana
      1, // Guinea
      1, // Guinea-Bissau
      1, // Ivory Coast
      1, // Kenya
      1, // Lesotho
      1, // Liberia
      1, // Libya
      1, // Madagascar
      1, // Malawi
      1, // Mali
      1, // Mauritania
      1, // Mauritius
      1, // Morocco
      1, // Mozambique
      1, // Namibia
      1, // Niger
      1, // Nigeria
      1, // Rwanda
      1, // Sao Tome and Principe
      1, // Senegal
      1, // Seychelles
      1, // Sierra Leone
      1, // Somalia
      1, // South Africa
      1, // South Sudan
      1, // Sudan
      1, // Tanzania
      1, // Togo
      1, // Tunisia
      1, // Uganda
      1, // Zambia
      1, // Zimbabwe
      1, // Australia
      1, // United States of America
    ],
    totalUser: 1300,
    data: [
      { id: 'Australia', name: 'Australia', value: 78 },
      { id: 'Europe', name: 'Europe', value: 580 },
      { id: 'Asia', name: 'Asia', value: 103 },
      { id: 'Africa', name: 'Africa', value: 239 },
      { id: 'America', name: 'America', value: 78 },
    ],
  },
  knowledgeGraph: {
    title: 'Knowledge Graph',
    subTitle: 'Knowledge Graph',
    data: {
      nodes: [
        { id: 'Node 1', group: 1 },
        { id: 'Node 2', group: 1 },
        { id: 'Node 3', group: 2 },
        { id: 'Node 4', group: 2 },
        { id: 'Node 5', group: 2 },
        { id: 'Node 6', group: 2 },
        { id: 'Node 7', group: 2 },
        { id: 'Node 8', group: 2 },
      ]
      ,
      links:
        [
          { source: 'Node 1', target: 'Node 2', value: 10 },
          { source: 'Node 1', target: 'Node 3', value: 20 },
          { source: 'Node 3', target: 'Node 4', value: 30 },
          { source: 'Node 2', target: 'Node 5', value: 10 },
          { source: 'Node 2', target: 'Node 6', value: 50 },
        ]
      ,
    }
  },
  keywordsDistribution: {
    title: 'Keywords Distribution',
    subTitle: "Probability Distribution of keywords of the selected topic",
    data: [
      {
        name: "need",
        value: 0.028510894626379013
      },
      {
        name: "feel",
        value: 0.013326014392077923
      },
      {
        name: "like",
        value: 0.012375205755233765
      },
      {
        name: "game",
        value: 0.011271191760897636
      },
      {
        name: "person",
        value: 0.010939954780042171
      },
      {
        name: "time",
        value: 0.010890712030231953
      },
      {
        name: "home",
        value: 0.01051084604114294
      },
      {
        name: "sleep",
        value: 0.00957251712679863
      },
      {
        name: "thing",
        value: 0.009436240419745445
      },
      {
        name: "help",
        value: 0.008520175702869892
      }
    ],
  },
  analyticsAgeBox: {
    title: ' Mental Health Tweets by Age Group',
    subTitle: 'Age Insights on Mental Health Tweets',
    dataChart: {
      totalData: '1.5M',
      dateStart: "Sep 15",
      dateEnd: "Sep 18",
      LegendList: [
        { title: 'Under 18', color: ColorVar.blue },
        { title: '19 - 29', color: ColorVar.green },
        { title: '30 - 39', color: ColorVar.orange },
        { title: '40 and above', color: ColorVar.red },
      ],
      dataLineChart: [
        {
          total: '1.5M',
          color: ColorVar.blue,
          data: [
            {
              '<=18': 1246,
              '19-29': 2400,
              '30-39': 3723,
              '>=40': 2100,
            },
            {
              '<=18': 2535,
              '19-29': 1398,
              '30-39': 2342,
              '>=40': 2450,
            },
            {
              '<=18': 1356,
              '19-29': 2583,
              '30-39': 568,
              '>=40': 1820,
            },
            {
              '<=18': 3421,
              '19-29': 1000,
              '30-39': 1200,
              '>=40': 1785,
            },
            {
              '<=18': 2525,
              '19-29': 2356,
              '30-39': 2345,
              '>=40': 2357,
            },
            {
              '<=18': 2561,
              '19-29': 2352,
              '30-39': 2356,
              '>=40': 1246,
            },
            {
              '<=18': 657,
              '19-29': 5464,
              '30-39': 3467,
              '>=40': 2461,
            },
          ],
        },
      ],
    },
  },
  analyticsSentimentBox: {
    title: ' Mental Health Tweets by Sentiment Analysis Result',
    subTitle: 'Sentiment Insights on Mental Health Tweets',
    dataChart: {
      totalData: '1.5M',
      dateStart: "Sep 15",
      dateEnd: "Sep 18",
      LegendList: [
        { title: 'Positive', color: ColorVar.green },
        { title: 'Neutral', color: ColorVar.blue },
        { title: 'Negative', color: ColorVar.orange },
      ],
      dataLineChart: [
        {
          data: [
            {
              Positive: 152,
              Negative: 141,
              Neutral: 135,
            },
            {
              Positive: 153,
              Negative: 155,
              Neutral: 160,
            },
            {
              Positive: 112,
              Negative: 135,
              Neutral: 125,
            },
            {
              Positive: 155,
              Negative: 135,
              Neutral: 126,
            },
            {
              Positive: 145,
              Negative: 115,
              Neutral: 146,
            },
            {
              Positive: 124,
              Negative: 145,
              Neutral: 145,
            },
            {
              Positive: 145,
              Negative: 142,
              Neutral: 123,
            },
          ],
        },
      ],
    },
  },
  analyticsGenderBox: {
    title: ' Mental Health Tweets by Gender',
    subTitle: 'Gender Insights on Mental Health Tweets',
    dataChart: {
      dateStart: "Sep 15",
      dateEnd: "Sep 18",
      LegendList: [
        { title: 'Female', color: ColorVar.red },
        { title: 'Male', color: ColorVar.blue },
      ],
      dataLineChart: [

        {
          data: [
            {
              Female: 46,
              Male: 24,
            },
            {
              Female: 39,
              Male: 23,

            },
            {
              Female: 46,
              Male: 26,
            },
            {
              Female: 55,
              Male: 34,
            },
            {
              Female: 56,
              Male: 40,
            },
            {
              Female: 52,
              Male: 24,
            },
            {
              Female: 23,
              Male: 62,
            },
          ],
        },
      ],
    },
  }

};