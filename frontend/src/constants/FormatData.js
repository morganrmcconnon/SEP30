import DATATYPES from "./dataTypes";

function display_backend_data_into_age_groups(backend_data) {
  let aggregated_result = backend_data['aggregated_result'];
  let age_groups_count = aggregated_result['age_groups_count'];
  let d1 = age_groups_count["<=18"];
  let d2 = age_groups_count["19-29"];
  let d3 = age_groups_count["30-39"];
  let d4 = age_groups_count[">=40"];

  let p1 = d1 / (d1 + d2 + d3 + d4) * 100;
  let p2 = d2 / (d1 + d2 + d3 + d4) * 100;
  let p3 = d3 / (d1 + d2 + d3 + d4) * 100;
  let p4 = d4 / (d1 + d2 + d3 + d4) * 100;

  // Round to 2 decimal places
  p1 = Math.round(p1 * 100) / 100;
  p2 = Math.round(p2 * 100) / 100;
  p3 = Math.round(p3 * 100) / 100;
  p4 = Math.round(p4 * 100) / 100;

  DATATYPES.agegroups.data.forEach(element => {
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

function display_backend_data_into_genders(backend_data) {
  let aggregated_result = backend_data['aggregated_result'];
  let genders_count = aggregated_result['genders_count'];

  DATATYPES.genders.data.female.present = genders_count['female'];
  DATATYPES.genders.data.male.present = genders_count['male'];
  return DATATYPES;
}


// Given coordinates, return the country name in topojson
function getCountryNameFromCoordinates(coordinates) {
}

function display_backend_data_into_locations(backend_data) {
  const aggregated_result = backend_data['aggregated_result'];
  const countries_count = aggregated_result['countries_count'];
  DATATYPES.locations.locationHighLight = Object.keys(countries_count);

  
  
  let locations = Object.entries(countries_count).map(([country, country_count]) => {
    return { name: country, value: country_count };
  }).sort((a, b) => b.value - a.value);
  
  // put the value of the country named "AUS" to the top of the array
  let index = locations.findIndex((element) => element.name === "");
  let temp = locations[0];
  temp.name = "Country not found";
  // Remove the element at index
  locations.splice(index, 1);
  // Add the element at index 0
  locations.unshift(temp);

  DATATYPES.locations.data = locations.splice(0, 5);

  return DATATYPES;
}


function display_backend_data_into_topicModelling(backend_data) {

  let aggregated_result = backend_data['aggregated_result'];
  let topics_count = aggregated_result['topics_count'];

  // For each key value pair in topics_count, add a new object to the data array
  DATATYPES.topicModelling.data = Object.entries(topics_count).map(([topic, topic_count]) => {
    return { date: Date.now(), topic: topic, mentionTimes: topic_count };
  });

  return DATATYPES;
}


function display_backend_data_into_sentimentAnalysis(backend_data) {
  let aggregated_result = backend_data['aggregated_result'];
  let sentiment_count = aggregated_result['sentiment_count'];

  DATATYPES.sentimentAnalysis.values.positive = sentiment_count['positive'];
  DATATYPES.sentimentAnalysis.values.neutral = sentiment_count['neutral'];
  DATATYPES.sentimentAnalysis.values.negative = sentiment_count['negative'];

  DATATYPES.sentimentAnalysis.data.forEach(element => {
    element.value = DATATYPES.sentimentAnalysis.values[element.value_key];
  });
  
  return DATATYPES;
}


function display_backend_data_into_analyticsBox(backend_data) {

  const tweets_amount_info = backend_data['tweets_amount_info'];
  const analysis_timestamps = tweets_amount_info['analysis_timestamps'];

  DATATYPES.analyticsBox.dataChart.totalData = tweets_amount_info['total_tweets_count'];


  DATATYPES.analyticsBox.dataBoxRight[0].title = 'Mental health tweets';
  DATATYPES.analyticsBox.dataBoxRight[0].total = tweets_amount_info['total_tweets_count'];
  DATATYPES.analyticsBox.dataBoxRight[0].value = tweets_amount_info['mental_health_related_tweets_count'];
  DATATYPES.analyticsBox.dataBoxRight[1].title = 'Displaying analysis of';
  DATATYPES.analyticsBox.dataBoxRight[1].total = tweets_amount_info['mental_health_related_tweets_count'];
  DATATYPES.analyticsBox.dataBoxRight[1].value = tweets_amount_info['mental_health_related_tweets_count']
  return DATATYPES;
}


function display_backend_data_into_top5Trends(backend_data) {

}


function display_backend_data_into_knowledge_graph(backend_data) {

  let aggregated_result = backend_data['aggregated_result'];
  let keywords_count = aggregated_result['keywords_count'];
  let keywords_pairs = aggregated_result['keywords_pairs'];
  let topic_values = backend_data['topic_values'];
  DATATYPES.knowledgeGraph.data = {
    nodes: Object.entries(keywords_count).map(([keyword, count]) => { return { 'id': keyword, 'group': 2, 'value': count }; }),
    links: keywords_pairs.map((keywords_pair_obj) => {
      return {
        'source': keywords_pair_obj["keywords"][0],
        'target': keywords_pair_obj["keywords"][1],
        'value': keywords_pair_obj["count"]
      };
    })
  };
  return DATATYPES;

}


export default function display_backend_data_into_charts(backend_data) {

  console.log("DATATYPES before display_backend_data_into_charts");
  console.log(DATATYPES);

  display_backend_data_into_analyticsBox(backend_data);
  display_backend_data_into_sentimentAnalysis(backend_data);
  display_backend_data_into_topicModelling(backend_data);
  display_backend_data_into_age_groups(backend_data);
  display_backend_data_into_genders(backend_data);
  display_backend_data_into_locations(backend_data);
  display_backend_data_into_top5Trends(backend_data);
  display_backend_data_into_knowledge_graph(backend_data);
  console.log("DATATYPES after display_backend_data_into_charts");
  console.log(DATATYPES);

  return DATATYPES;
}