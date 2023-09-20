export default interface TweetObject {
  "created_at": string,
  "id": number,
  "id_str": string,
  "text": string,
  "display_text_range": [number, number],
  "source": string,
  "truncated": boolean,
  "in_reply_to_status_id": number,
  "in_reply_to_status_id_str": string,
  "in_reply_to_user_id": number,
  "in_reply_to_user_id_str": string,
  "in_reply_to_screen_name": string,
  "user": {
    "id": number,
    "id_str": string,
    "name": string,
    "screen_name": string,
    "location": string,
    "url": string,
    "description": string,
    "translator_type": string,
    "protected": boolean,
    "verified": boolean,
    "followers_count": number,
    "friends_count": number,
    "listed_count": number,
    "favourites_count": number,
    "statuses_count": number,
    "created_at": string,
    "utc_offset": string | null,
    "time_zone": string | null,
    "geo_enabled": boolean,
    "lang": string | null,
    "contributors_enabled": boolean,
    "is_translator": boolean,
    "profile_background_color": string | null,
    "profile_background_image_url": string | null,
    "profile_background_image_url_https": string | null,
    "profile_background_tile": boolean,
    "profile_link_color": string | null,
    "profile_sidebar_border_color": string | null,
    "profile_sidebar_fill_color": string | null,
    "profile_text_color": string | null,
    "profile_use_background_image": boolean,
    "profile_image_url": string | null,
    "profile_image_url_https": string | null,
    "profile_banner_url": string | null,
    "default_profile": boolean,
    "default_profile_image": boolean,
    "following": string | null,
    "follow_request_sent": string | null,
    "notifications": string | null,
    "withheld_in_countries": []
  },
  "geo": string | null,
  "coordinates": string | null,
  "place": string | null,
  "contributors": string | null,
  "is_quote_status": boolean,
  "extended_tweet": {
    "full_text": string,
    "display_text_range": [number, number],
    "entities": Object,
    "extended_entities": Object,
  },
  "quote_count": number,
  "reply_count": number,
  "retweet_count": number,
  "favorite_count": number,
  "entities": Object,
  "favorited": boolean,
  "retweeted": boolean,
  "possibly_sensitive": boolean,
  "filter_level": string,
  "lang": string,
  "timestamp_ms": string,
  "text_analyzed": {
    "original": string,
    "lang_detected": string,
    "processed": Array<string>,
    "sentiment": {
      "negative": number,
      "neutral": number,
      "positive": number,
    },
    "sentiment_predicted": string,
    "topics": Array<[number, number]>,
    "topic_with_the_highest_score": number,
    "associated_keywords": Array<string>,
  }
}