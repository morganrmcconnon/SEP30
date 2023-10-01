import { AgeGroupData, GenderData, SentimentData } from "../../api/types/constants";
import { DATATYPES } from "../constants/DATATYPES";


function update_age_groups_grid(age_groups_count: AgeGroupData) {
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


function update_genders_grid(genders_count: GenderData, female_sentiment: SentimentData | undefined = undefined, male_sentiment: SentimentData | undefined = undefined) {
  
  if (female_sentiment !== undefined) {
    DATATYPES.genders.data.female.sentiment = female_sentiment;
  } 
  
  DATATYPES.genders.data.female.present = genders_count['female'];
  
  if (male_sentiment !== undefined) {
    DATATYPES.genders.data.male.sentiment = male_sentiment;
  }
  
  DATATYPES.genders.data.male.present = genders_count['male'];
  
  return DATATYPES;
}


function update_map(countries_count: Record<string, number>, country_names: Record<string, string> = {}) {
  country_names[""] = "UNCATEGORISED";
  DATATYPES.locations.totalUser = Object.values(countries_count).reduce((a, b) => a + b, 0) - (countries_count[""] || 0);
  // DATATYPES.locations.totalUser = Object.values(countries_count).reduce((a, b) => a + b, 0);

  DATATYPES.locations.locationHighLight = Object.keys(countries_count);

  DATATYPES.locations.locationHighLightData = Object.values(countries_count);

  let locations = Object.entries(countries_count).map(([country_code, country_count]) => {
    return { id: country_code, name: country_names[country_code], value: country_count };
  }).sort((a, b) => b.value - a.value).filter((element) => element.id !== "");


  // // put the value of the country named "AUS" to the top of the array
  let index = locations.findIndex((element) => element.id === "AUS");
  
  if (index != -1){
	  let temp = locations[index];
	  // Remove the element at index
	  locations.splice(index, 1);
	  // Add the element to the top of the array
    locations.unshift(temp);
  }
  
  DATATYPES.locations.data = locations.splice(0, 5);

  return DATATYPES;
}


function update_topic_modelling_grid(topics_count: Record<string, number>) {

  // For each key value pair in topics_count, add a new object to the data array
  DATATYPES.topicModelling.data = Object.entries(topics_count).map(([topic, topic_count]) => {
    return { date: Date.now(), topic: topic, mentionTimes: topic_count };
  });

  return DATATYPES;
}


function update_sentimentAnalysis_grids(sentiment_count: SentimentData) {

  DATATYPES.sentimentAnalysis.values.positive = sentiment_count['positive'];
  DATATYPES.sentimentAnalysis.values.neutral = sentiment_count['neutral'];
  DATATYPES.sentimentAnalysis.values.negative = sentiment_count['negative'];

  DATATYPES.sentimentAnalysis.data.forEach(element => {
    element.value = DATATYPES.sentimentAnalysis.values[element.value_key];
  });

  return DATATYPES;
}


function update_analyticsBox(total_tweets_count: number, mental_health_related_tweets_count: number, tweets_displayed_count: number) {

  DATATYPES.analyticsBox.dataChart.totalData = total_tweets_count.toString();


  DATATYPES.analyticsBox.dataBoxRight[0].title = 'Mental health tweets';
  DATATYPES.analyticsBox.dataBoxRight[0].total = total_tweets_count;
  DATATYPES.analyticsBox.dataBoxRight[0].value = mental_health_related_tweets_count;
  DATATYPES.analyticsBox.dataBoxRight[1].title = 'Displaying analysis of';
  DATATYPES.analyticsBox.dataBoxRight[1].total = mental_health_related_tweets_count;
  DATATYPES.analyticsBox.dataBoxRight[1].value = tweets_displayed_count;
  return DATATYPES;
}

// function display_backend_data_into_analyticsSentimentBox(total_tweets_count: number, mental_health_related_tweets_count: number, tweets_displayed_count: number) {



//   return DATATYPES;
// }

// function display_backend_data_into_analyticsGenderBox(total_tweets_count: number, mental_health_related_tweets_count: number, tweets_displayed_count: number) {

 

//    return DATATYPES;
// }

// function display_backend_data_into_analyticsAgeBox(total_tweets_count: number, mental_health_related_tweets_count: number, tweets_displayed_count: number) {

  
//   return DATATYPES;
// }

function update_knowledge_graph(keywords_count: Record<string, number>, keywords_pairs: Array<{ keywords: Array<string>, count: number }>) {

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


export function update_dashboard_data(
  total_tweets_count: number,
  mental_health_related_tweets_count: number,
  tweets_displayed_count: number,
  sentiment_count: SentimentData,
  topics_count: Record<string, number>,
  keywords_count: Record<string, number>,
  keywords_pairs: Array<{ keywords: Array<string>, count: number }>,
  countries_count: Record<string, number>,
  country_names: Record<string, string>,
  age_groups_count: AgeGroupData,
  genders_count: GenderData,
  female_sentiment : SentimentData, 
  male_sentiment : SentimentData,
) {

  update_analyticsBox(total_tweets_count, mental_health_related_tweets_count, tweets_displayed_count);
  // display_backend_data_into_analyticsAgeBox(total_tweets_count, mental_health_related_tweets_count, tweets_displayed_count);
  // display_backend_data_into_analyticsGenderBox(total_tweets_count, mental_health_related_tweets_count, tweets_displayed_count);
  // display_backend_data_into_analyticsSentimentBox(total_tweets_count, mental_health_related_tweets_count, tweets_displayed_count);

  update_topic_modelling_grid(topics_count);

  update_knowledge_graph(keywords_count, keywords_pairs);

  update_sentimentAnalysis_grids(sentiment_count);

  update_map(countries_count, country_names);

  update_age_groups_grid(age_groups_count);

  update_genders_grid(genders_count, female_sentiment, male_sentiment);

  return DATATYPES;
}
