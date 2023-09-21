import { TweetObject, SentimentData } from "./TweetObjectTypes"
import { AgeGroupData, GenderData, OrgData, UserObject } from "./UserObjectTypes"

export interface BackendOutputType {
  "analysis_timestamps": {
    "start_analysis_at": number,
    "complete_tweet_objects_analysis_at": number,
    "complete_user_objects_analysis_at": number,
    "complete_aggregating_tweet_objects_analysis_at": number,
    "complete_aggregating_user_objects_analysis_result_at": number,
    "end_analysis_at": number,
  },
  "tweets_amount_info": {
    "total_tweets_count": number,
    "mental_health_related_tweets_count": number,
    "analyzed_at": number,
  },
  "aggregated_result": {
    "sentiment_count": SentimentData,
    "topics_count": Record<string, number>,
    "countries_count": Record<string, number>,
    "genders_count": GenderData,
    "age_groups_count": AgeGroupData,
    "org_count": OrgData,
    "keywords_count": Record<string, number>,
    "keywords_pairs": Array<{ "keywords": Array<string>, "count": number }>,
  },
  "topics_values": Record<string, Array<[string, number]>>,
  "tweet_objects": Array<TweetObject>,
  "user_objects": Array<UserObject>
}

export const SAMPLEBACKENDOUTPUT = {
  "analysis_timestamps": {
    "start_analysis_at": 1694717064.3947034,
    "complete_tweet_objects_analysis_at": 1694717261.7680979,
    "complete_user_objects_analysis_at": 1694717300.0653508,
    "complete_aggregating_tweet_objects_analysis_at": 1694717300.0738697,
    "complete_aggregating_user_objects_analysis_result_at": 1694717300.0788915,
    "end_analysis_at": 1694717300.079955
  },
  "tweets_amount_info": {
    "total_tweets_count": 11152,
    "mental_health_related_tweets_count": 21,
    "analyzed_at": 1694717300.0758693
  },
  "aggregated_result": {
    "sentiment_count": { "negative": 21, "positive": 0, "neutral": 0 },
    "topics_count": { "0": 3, "1": 4, "2": 0, "3": 2, "4": 2, "5": 1, "6": 4, "7": 0, "8": 3, "9": 2 },
    "countries_count": { "GBR": 1, "USA": 2, "": 13, "NZL": 1, "CAN": 1, "CHN": 1, "VNM": 2 },
    "genders_count": { "female": 13, "male": 8 },
    "age_groups_count": { "19-29": 3, "30-39": 3, "<=18": 12, ">=40": 3 },
    "org_count": { "is-org": 0, "non-org": 9 },
    "keywords_count": { "amp": 3, "life": 1, "health": 5, "mental": 1, "cat": 1, "year": 1, "win": 2, "real": 2, "hard": 1, "person": 1, "good": 1, "so": 9, "time": 4, "love": 5, "man": 1, "like": 1, "bitch": 1, "shit": 1, "way": 1, "pain": 1 },
    "keywords_pairs": [
      { "keywords": ["amp", "life"], "count": 1 },
      { "keywords": ["amp", "health"], "count": 2 },
      { "keywords": ["amp", "mental"], "count": 1 },
      { "keywords": ["health", "life"], "count": 1 },
      { "keywords": ["life", "mental"], "count": 1 },
      { "keywords": ["health", "mental"], "count": 1 },
      { "keywords": ["amp", "cat"], "count": 1 },
      { "keywords": ["amp", "year"], "count": 1 },
      { "keywords": ["amp", "win"], "count": 2 },
      { "keywords": ["cat", "health"], "count": 1 },
      { "keywords": ["cat", "year"], "count": 1 },
      { "keywords": ["cat", "win"], "count": 1 },
      { "keywords": ["health", "year"], "count": 1 },
      { "keywords": ["health", "win"], "count": 1 },
      { "keywords": ["win", "year"], "count": 1 },
      { "keywords": ["hard", "real"], "count": 1 },
      { "keywords": ["good", "person"], "count": 1 },
      { "keywords": ["person", "so"], "count": 1 },
      { "keywords": ["good", "so"], "count": 1 },
      { "keywords": ["love", "time"], "count": 3 },
      { "keywords": ["so", "time"], "count": 4 },
      { "keywords": ["health", "time"], "count": 3 },
      { "keywords": ["love", "so"], "count": 5 },
      { "keywords": ["health", "love"], "count": 3 },
      { "keywords": ["health", "so"], "count": 3 },
      { "keywords": ["love", "man"], "count": 1 },
      { "keywords": ["man", "so"], "count": 1 },
      { "keywords": ["bitch", "like"], "count": 1 },
      { "keywords": ["love", "way"], "count": 1 },
      { "keywords": ["so", "way"], "count": 1 },
      { "keywords": ["amp", "so"], "count": 1 },
      { "keywords": ["amp", "pain"], "count": 1 },
      { "keywords": ["pain", "so"], "count": 1 },
      { "keywords": ["so", "win"], "count": 1 },
      { "keywords": ["pain", "win"], "count": 1 }
    ]
  },
  "topics_values": {
    '0' : [
      ["need", 0.028510894626379013],
      ["feel", 0.013326014392077923],
      ["like", 0.012375205755233765],
      ["game", 0.011271191760897636],
      ["person", 0.010939954780042171],
      ["time", 0.010890712030231953],
      ["home", 0.01051084604114294],
      ["sleep", 0.00957251712679863],
      ["thing", 0.009436240419745445],
      ["help", 0.008520175702869892]
    ],
    '1' : [
      ["lol", 0.01682061143219471],
      ["positive", 0.0161189753562212],
      ["thought", 0.01592232659459114],
      ["thinking", 0.015082203783094883],
      ["tweet", 0.014364149421453476],
      ["amp", 0.012759528122842312],
      ["cat", 0.010784784331917763],
      ["tonight", 0.008931872434914112],
      ["minute", 0.00870587956160307],
      ["okay", 0.008650736883282661]
    ],
    '2' : [
      ["talk", 0.024411169812083244],
      ["friend", 0.02216077223420143],
      ["gonna", 0.017967404797673225],
      ["thing", 0.01756245084106922],
      ["god", 0.01703547313809395],
      ["good", 0.015826398506760597],
      ["hour", 0.01374959759414196],
      ["strong", 0.010126476176083088],
      ["stay", 0.010083477012813091],
      ["business", 0.009595368057489395]
    ],
    '3' : [
      ["depression", 0.032392702996730804],
      ["look", 0.026487410068511963],
      ["fuck", 0.024080999195575714],
      ["treatment", 0.012174401432275772],
      ["fucking", 0.011066149920225143],
      ["like", 0.010754884220659733],
      ["hard", 0.01027251873165369],
      ["damn", 0.009971440769731998],
      ["diagnosed", 0.00987349171191454],
      ["life", 0.008854557760059834]
    ],
    '4' : [
      ["love", 0.0356631875038147],
      ["got", 0.019419420510530472],
      ["yeah", 0.016526149585843086],
      ["night", 0.015509234741330147],
      ["happy", 0.015110064297914505],
      ["day", 0.012606591917574406],
      ["so", 0.010862835682928562],
      ["real", 0.009937955066561699],
      ["mean", 0.009861725382506847],
      ["man", 0.009702591225504875]
    ],
    '5' : [
      ["great", 0.016228443011641502],
      ["yes", 0.014471115544438362],
      ["guy", 0.012205829843878746],
      ["stop", 0.010456540621817112],
      ["tell", 0.010402265004813671],
      ["people", 0.009282199665904045],
      ["fan", 0.009089954197406769],
      ["day", 0.008946718648076057],
      ["gotta", 0.008707533590495586],
      ["tomorrow", 0.008575853891670704]
    ],
    '6' : [
      ["like", 0.03394567221403122],
      ["think", 0.025675088167190552],
      ["shit", 0.020526211708784103],
      ["right", 0.017264656722545624],
      ["people", 0.014911887235939503],
      ["health", 0.009814760647714138],
      ["mental", 0.009404337033629417],
      ["know", 0.009231487289071083],
      ["bitch", 0.008781665936112404],
      ["feel", 0.007768768817186356]
    ],
    '7' : [
      ["migraine", 0.03809652104973793],
      ["girl", 0.022534508258104324],
      ["want", 0.016389373689889908],
      ["year", 0.015422159805893898],
      ["pretty", 0.014400074258446693],
      ["sure", 0.011955203488469124],
      ["worth", 0.010902885347604752],
      ["vegan", 0.010889638215303421],
      ["help", 0.010752617381513119],
      ["pain", 0.010538902133703232]
    ],
    '8' : [
      ["depression", 0.06099637597799301],
      ["treatment", 0.022971954196691513],
      ["overcome", 0.018580924719572067],
      ["know", 0.013619773089885712],
      ["anxiety", 0.012038345448672771],
      ["amp", 0.009726385585963726],
      ["suicide", 0.009376998990774155],
      ["disorder", 0.007307791151106358],
      ["health", 0.007077227812260389],
      ["start", 0.006799325346946716]
    ],
    '9' : [
      ["way", 0.03640351817011833],
      ["headache", 0.028295552358031273],
      ["actually", 0.02427435666322708],
      ["change", 0.01400669477880001],
      ["win", 0.009722189977765083],
      ["away", 0.009632869623601437],
      ["world", 0.008552656508982182],
      ["literally", 0.007851555943489075],
      ["remedy", 0.007600277662277222],
      ["best", 0.006496726535260677]
    ]
  },
  "tweet_objects": [],
  "user_objects": []
}