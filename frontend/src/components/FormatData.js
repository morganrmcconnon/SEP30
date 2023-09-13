import DATATYPES from "../constants/dataTypes";

function display_backend_data_into_demographics1(backend_data) {
  let d1 = backend_data[5]["<=18"];
  let d2 = backend_data[5]["19-29"];
  let d3 = backend_data[5]["30-39"];
  let d4 = backend_data[5][">=40"];

  let p1 = d1 / (d1 + d2 + d3 + d4) * 100;
  let p2 = d2 / (d1 + d2 + d3 + d4) * 100;
  let p3 = d3 / (d1 + d2 + d3 + d4) * 100;
  let p4 = d4 / (d1 + d2 + d3 + d4) * 100;

  // Round to 2 decimal places
  p1 = Math.round(p1 * 100) / 100;
  p2 = Math.round(p2 * 100) / 100;
  p3 = Math.round(p3 * 100) / 100;
  p4 = Math.round(p4 * 100) / 100;

  DATATYPES.demoGraphic1.data.forEach(element => {
    switch (element.name) {
      case 'Under 18':
        element.percent = p1;
        break;
      case '19 - 29':
        element.percent = p2;
        break;
      case '30 - 39':
        element.percent = p3;
        break;
      case '40 and above':
        element.percent = p4;
        break;
      default:
        break;
    }
  });

  return DATATYPES;
}

function display_backend_data_into_demographics2(backend_data) {
  DATATYPES.demoGraphic2.data.female.present = backend_data[0]['female'];
  DATATYPES.demoGraphic2.data.male.present = backend_data[0]['male'];
  return DATATYPES;
}

function display_backend_data_into_demographics3(backend_data) {
  return DATATYPES;
}


function display_backend_data_into_topicModelling(backend_data) {
  for (let i = 0; i < 5; i++) {
    DATATYPES.topicModelling.data[i].mentionTimes = backend_data[0][i.toString()];
  }

  return DATATYPES;
}


function display_backend_data_into_sentimentAnalysis(backend_data) {
  DATATYPES.sentimentAnalysis.data = [
    { title: 'Positive Tweets', subTitle: 'Number of positive tweets', star: backend_data[1]['positive'] },
    { title: 'Negative Tweets', subTitle: 'Number of negative tweets', star: backend_data[1]['negative'] },
    { title: 'Neutral Tweets', subTitle: 'Number of neutral tweets', star: backend_data[1]['neutral'] },
  ];

  return DATATYPES;
}


function display_backend_data_into_analyticsBox(backend_data) {
  [
    {
      title: 'Total Tweets',
      value: backend_data[2]['total'], 
      total: backend_data[2]['total'], 
      colorChart: 'white', 
      bgColor: '#339af0', 
      textColor: 'white'
    },
    {
      title: 'Related Tweets',
      value: backend_data[2]['mentalhealthtweets'],
      total: backend_data[2]['total'],
      colorChart: ColorVar.orange,
      bgColor: 'white',
      textColor: '#000',
    },
  ],
  DATATYPES.analyticsBox.dataBoxRight[0].title = 'total';
  DATATYPES.analyticsBox.dataBoxRight[0].total = backend_data[2]['total'];
  DATATYPES.analyticsBox.dataBoxRight[0].value = backend_data[2]['total'];
  DATATYPES.analyticsBox.dataBoxRight[1].title = 'mental health tweets';
  DATATYPES.analyticsBox.dataBoxRight[1].total = backend_data[2]['total'];
  DATATYPES.analyticsBox.dataBoxRight[1].value = backend_data[2]['mentalhealthtweets'];
  return DATATYPES;
}


function display_backend_data_into_top5Trends(backend_data) {

}


export default function display_backend_data_into_charts(backend_data) {

  display_backend_data_into_demographics1(backend_data);
  display_backend_data_into_demographics2(backend_data);
  display_backend_data_into_demographics3(backend_data);
  display_backend_data_into_topicModelling(backend_data);
  display_backend_data_into_sentimentAnalysis(backend_data);
  display_backend_data_into_analyticsBox(backend_data);
  display_backend_data_into_top5Trends(backend_data);

  return DATATYPES;
}