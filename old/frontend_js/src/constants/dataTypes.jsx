import dayjs from "dayjs";
import { BsArrowRight } from "react-icons/bs";

import ColorVar from "./ColorVar";

const DATATYPES = {
  analyticsBox: {
    title: "Real-time Analysis",
    subTitle: "Real-time Analysis results",
    dataChart: {
      totalData: "1.5M",
      totalDataChange: "-0.8%",
      dateStart: "Dec19",
      dateEnd: "Dec25",
      LegendList: [
        { title: "Total", color: ColorVar.blue },
        { title: "CTG1", color: ColorVar.green },
        { title: "CTG2", color: ColorVar.orange },
      ],
      dataLineChart: [
        {
          total: "1.5M",
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
          total: "1.1M",
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
          total: "608K",
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
        title: "Related Tweets",
        value: 1602,
        total: 2000,
        colorChart: "white",
        bgColor: ColorVar.blue,
        textColor: "white",
      },
      {
        title: "Displaying",
        value: 1255,
        total: 2000,
        colorChart: ColorVar.orange,
        bgColor: "white",
        textColor: "#000",
      },
    ],
  },
  top5Trends: {
    title: "Top 5 Trends",
    subTitle: "Update by",
    data: [
      {
        title: "Trend 1",
        subTitle: "Subtitle",
        year: "2020",
        date: Date.now(),
        status: "up",
        topTrend: true,
      },
      {
        title: "Trend 2",
        subTitle: "Subtitle",
        year: "2020",
        date: Date.now(),
        status: "up",
        topTrend: false,
      },
      {
        title: "Trend 3",
        subTitle: "Subtitle",
        year: "2020",
        date: Date.now(),
        status: "up",
        topTrend: false,
      },
      {
        title: "Trend 4",
        subTitle: "Subtitle",
        year: "2020",
        date: Date.now(),
        status: "down",
        topTrend: false,
      },
      {
        title: "Trend 5",
        subTitle: "Subtitle",
        year: "2020",
        date: Date.now(),
        status: "down",
        topTrend: false,
      },
      {
        title: "Trend 6",
        subTitle: "Subtitle",
        year: "2020",
        date: Date.now(),
        status: "down",
        topTrend: false,
      },
    ],
  },
  topicModelling: {
    title: "Topic modelling",
    subTitle: "Topic modelling result",
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
        title: "Topic",
        dataIndex: "topic",
        key: "topic",
        // specify the condition of filtering result
        // here is that finding the name started with `value`
        onFilter: (value, record) => record.name.indexOf(value) === 0,
        sorter: (a, b) => a.topic.length - b.topic.length,
      },
      {
        title: "Number of tweets",
        dataIndex: "mentionTimes",
        key: "mentionTimes",
        render: (mentionTimes) => (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <p>{mentionTimes}</p>
            <BsArrowRight />
          </div>
        ),
        sorter: (a, b) => a.mentionTimes - b.mentionTimes,
      },
    ],
    data: [
      { date: Date.now(), topic: "Topic 1", mentionTimes: 1000 },
      { date: Date.now(), topic: "Topic 2", mentionTimes: 900 },
      { date: Date.now(), topic: "Topic 3", mentionTimes: 800 },
      { date: Date.now(), topic: "Topic 4", mentionTimes: 700 },
      { date: Date.now(), topic: "Topic 5", mentionTimes: 600 },
      { date: Date.now(), topic: "Topic 6", mentionTimes: 500 },
      { date: Date.now(), topic: "Topic 7", mentionTimes: 300 },
      { date: Date.now(), topic: "Topic 8", mentionTimes: 200 },
      { date: Date.now(), topic: "Topic 9", mentionTimes: 100 },
    ],
  },
  sentimentAnalysis: {
    title: "Sentiment Analysis",
    subTitle: "Sentiment Analysis",
    values: {
      positive: 100,
      negative: 50,
      neutral: 50,
    },
    data: [
      {
        value_key: "positive",
        title: "Positive Tweets",
        subTitle: "Number of positive tweets",
        value: 199,
        color: ColorVar.green,
      },
      {
        value_key: "neutral",
        title: "Neutral Tweets",
        subTitle: "Number of neutral tweets",
        value: 50,
        color: ColorVar.blue,
      },
      {
        value_key: "negative",
        title: "Negative Tweets",
        subTitle: "Number of negative tweets",
        value: 100,
        color: ColorVar.orange,
      },
    ],
  },
  agegroups: {
    title: "Demographic Analysis - Age Groups",
    subTitle: "Age Groups percentage",
    data: [
      { name: "Under 18", percent: 18, color: ColorVar.blue },
      { name: "19 - 29", percent: 40, color: "#50cc65" },
      { name: "30 - 39", percent: 15, color: ColorVar.orange },
      { name: "40 and above", percent: 15, color: "#eeeeef" },
    ],
  },
  genders: {
    title: "Demographic Analysis - Genders",
    subTitle: "Demographic Analysis - Genders",
    data: {
      female: {
        present: 60,
        sentiment: {
          positive: 3,
          neutral: 9,
          negative: 11,
        },
        color: "#d3f9d8",
        activeList: ["1", "2", "3", "4"],
      },
      male: {
        present: 40,
        sentiment: {
          positive: 5,
          neutral: 2,
          negative: 9,
        },
        color: "#d0ebff",
        activeList: ["5", "6", "7", "8"],
      },
    },
  },
  locations: {
    title: "Demographic Analysis - Location",
    subTitle: "Demographic Analysis - Location",
    locationHighLight: [
      "DEU", // Germany
      "FRA", // France
      "ITA", // Italy
      "ESP", // Spain
      "GBR", // United Kingdom
      "GRC", // Greece
      "PRT", // Portugal
      "NLD", // Netherlands
      "BEL", // Belgium
      "AUT", // Austria
      "CHE", // Switzerland
      "SWE", // Sweden
      "NOR", // Norway
      "DNK", // Denmark
      "FIN", // Finland
      "POL", // Poland
      "RUS", // Russia
      "UKR", // Ukraine
      "CZE", // Czech Republic
      "SVK", // Slovakia
      "HUN", // Hungary
      "AFG", // Afghanistan
      "ARM", // Armenia
      "AZE", // Azerbaijan
      "BHR", // Bahrain
      "BGD", // Bangladesh
      "BTN", // Bhutan
      "BRN", // Brunei
      "KHM", // Cambodia
      "CHN", // China
      "CYP", // Cyprus
      "GEO", // Georgia
      "IND", // India
      "IDN", // Indonesia
      "IRN", // Iran
      "IRQ", // Iraq
      "ISR", // Israel
      "JPN", // Japan
      "JOR", // Jordan
      "KAZ", // Kazakhstan
      "KGZ", // Kyrgyzstan
      "KWT", // Kuwait
      "LAO", // Laos
      "LBN", // Lebanon
      "MYS", // Malaysia
      "MDV", // Maldives
      "MNG", // Mongolia
      "MMR", // Myanmar (Burma)
      "NPL", // Nepal
      "OMN", // Oman
      "PAK", // Pakistan
      "PHL", // Philippines
      "QAT", // Qatar
      "SAU", // Saudi Arabia
      "SGP", // Singapore
      "KOR", // South Korea
      "LKA", // Sri Lanka
      "SYR", // Syria
      "TWN", // Taiwan
      "TJK", // Tajikistan
      "THA", // Thailand
      "TLS", // Timor-Leste (East Timor)
      "TUR", // Turkey
      "TKM", // Turkmenistan
      "ARE", // United Arab Emirates
      "UZB", // Uzbekistan
      "VNM", // Vietnam
      "YEM", // Yemen
      "DZA", // Algeria
      "AGO", // Angola
      "BEN", // Benin
      "BWA", // Botswana
      "BFA", // Burkina Faso
      "BDI", // Burundi
      "CMR", // Cameroon
      "CPV", // Cape Verde
      "CAF", // Central African Republic
      "TCD", // Chad
      "COM", // Comoros
      "COD", // Democratic Republic of the Congo
      "DJI", // Djibouti
      "EGY", // Egypt
      "GNQ", // Equatorial Guinea
      "ERI", // Eritrea
      "SWZ", // Eswatini (formerly Swaziland)
      "ETH", // Ethiopia
      "GAB", // Gabon
      "GMB", // Gambia
      "GHA", // Ghana
      "GIN", // Guinea
      "GNB", // Guinea-Bissau
      "CIV", // Ivory Coast
      "KEN", // Kenya
      "LSO", // Lesotho
      "LBR", // Liberia
      "LBY", // Libya
      "MDG", // Madagascar
      "MWI", // Malawi
      "MLI", // Mali
      "MRT", // Mauritania
      "MUS", // Mauritius
      "MAR", // Morocco
      "MOZ", // Mozambique
      "NAM", // Namibia
      "NER", // Niger
      "NGA", // Nigeria
      "RWA", // Rwanda
      "STP", // Sao Tome and Principe
      "SEN", // Senegal
      "SYC", // Seychelles
      "SLE", // Sierra Leone
      "SOM", // Somalia
      "ZAF", // South Africa
      "SSD", // South Sudan
      "SDN", // Sudan
      "TZA", // Tanzania
      "TGO", // Togo
      "TUN", // Tunisia
      "UGA", // Uganda
      "ZMB", // Zambia
      "ZWE", // Zimbabwe
      "AUS", // Australia
      "USA", // United States of America
    ],
	locationHighLightData: [
     81, 42, 14, 59, 2, 75, 36, 64, 18, 97, 5, 70, 9, 88, 47, 38, 30, 65, 72, 90, 68, 7, 40, 83, 53, 24, 13, 79, 96, 35, 48, 86, 23, 10, 33, 54, 78, 58, 22, 84, 71, 16, 44, 93, 6, 95, 27, 62, 17, 45, 69, 3, 92, 32, 55, 77, 20, 66, 87, 21, 43, 76, 61, 31, 60, 74, 46, 15, 28, 89, 4, 51, 25, 56, 82, 67, 12, 37, 50, 29, 80, 49, 34, 11, 85, 19, 91, 63, 57, 26, 73, 1, 94, 52, 41, 8, 98, 39, 99, 2, 82, 49, 18, 63, 89, 3, 71, 45, 56, 8, 34, 94, 14, 66, 27, 95, 11, 68, 40, 21, 79, 36, 60, 87, 32, 70, 54, 25, 97, 48, 19, 50, 1, 75, 61, 12, 78, 5, 24, 90,
    ],
    totalUser: 1300,
    data: [
      { name: "Europe", value: 580 },
      { name: "Asia", value: 103 },
      { name: "Africa", value: 239 },
      { name: "Australia", value: 78 },
      { name: "America", value: 78 },
    ],
  },
  knowledgeGraph: {
    title: "Knowledge Graph",
    subTitle: "Knowledge Graph",
    data: {
      nodes: [
        { id: "Node 1", group: 1 },
        { id: "Node 2", group: 1 },
        { id: "Node 3", group: 2 },
        { id: "Node 4", group: 2 },
        { id: "Node 5", group: 2 },
        { id: "Node 6", group: 2 },
        { id: "Node 7", group: 2 },
        { id: "Node 8", group: 2 },
      ],
      links: [
        { source: "Node 1", target: "Node 2", value: 10 },
        { source: "Node 1", target: "Node 3", value: 20 },
        { source: "Node 3", target: "Node 4", value: 30 },
        { source: "Node 2", target: "Node 5", value: 10 },
        { source: "Node 2", target: "Node 6", value: 50 },
      ],
    },
  },
  keywordsDistribution: {
    title: "Keywords Distribution",
    subTitle: "Probability Distribution of keywords of the selected topic",
    data: [
      {
        name: "need",
        value: 0.028510894626379013,
      },
      {
        name: "feel",
        value: 0.013326014392077923,
      },
      {
        name: "like",
        value: 0.012375205755233765,
      },
      {
        name: "game",
        value: 0.011271191760897636,
      },
      {
        name: "person",
        value: 0.010939954780042171,
      },
      {
        name: "time",
        value: 0.010890712030231953,
      },
      {
        name: "home",
        value: 0.01051084604114294,
      },
      {
        name: "sleep",
        value: 0.00957251712679863,
      },
      {
        name: "thing",
        value: 0.009436240419745445,
      },
      {
        name: "help",
        value: 0.008520175702869892,
      },
    ],
  },
};

export default DATATYPES;
