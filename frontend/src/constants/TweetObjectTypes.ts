import { UserObject } from "./UserObjectTypes";

export type SentimentValue = "negative" | "neutral" | "positive";

export type SentimentData = { [value in SentimentValue] : number};


export type TweetObject = {
  "created_at": string,
  "id": number,
  "id_str": string,
  "user": UserObject,
  "text": string,
  // "display_text_range": [number, number],
  // "source": string,
  // "truncated": boolean,
  // "in_reply_to_status_id": number,
  // "in_reply_to_status_id_str": string,
  // "in_reply_to_user_id": number,
  // "in_reply_to_user_id_str": string,
  // "in_reply_to_screen_name": string,
  // "geo": string | null,
  // "coordinates": string | null,
  // "place": string | null,
  // "contributors": string | null,
  // "is_quote_status": boolean,
  // "extended_tweet": {
  //   "full_text": string,
  //   "display_text_range": [number, number],
  //   "entities": Object,
  //   "extended_entities": Object,
  // },
  // "quote_count": number,
  // "reply_count": number,
  // "retweet_count": number,
  // "favorite_count": number,
  // "entities": Object,
  // "favorited": boolean,
  // "retweeted": boolean,
  // "possibly_sensitive": boolean,
  // "filter_level": string,
  "lang": string,
  "timestamp_ms": string,
  "text_analyzed": {
    "original": string,
    "lang_detected": string,
    "in_english": string,
    "processed": Array<string>,
    "sentiment": { [value in SentimentValue]: number },
    "sentiment_predicted": SentimentValue,
    "topics": Array<[number, number]>,
    "topic_with_the_highest_score": number,
    "associated_keywords": Array<string>,
  }
}