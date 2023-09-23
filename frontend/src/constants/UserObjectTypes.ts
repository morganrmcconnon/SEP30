export type AgeGroupValue = "<=18" | "19-29" | "30-39" | ">=40";

export type GenderValue = "male" | "female";

export type OrgValue = "is-org" | "non-org";

export type AgeGroupData = Record<AgeGroupValue, number>;

export type GenderData = Record<GenderValue, number>;

export type OrgData = Record<OrgValue, number>;

export type UserObject = {
  "id": number,
  "id_str": string,
  "name": string,
  "screen_name": string,
  "description": string | null,
  "lang": string | null,
  "location": string | null,
  // "url": string | null,
  // "translator_type": string | null,
  // "protected": boolean,
  // "verified": boolean,
  // "followers_count": number,
  // "friends_count": number,
  // "listed_count": number,
  // "favourites_count": number,
  // "statuses_count": number,
  // "created_at": string,
  // "utc_offset": string | null,
  // "time_zone": string | null,
  // "geo_enabled": boolean,
  // "contributors_enabled": boolean,
  // "is_translator": boolean,
  // "profile_background_color": string | null,
  // "profile_background_image_url": string | null,
  // "profile_background_image_url_https": string | null,
  // "profile_background_tile": false,
  // "profile_link_color": string | null,
  // "profile_sidebar_border_color": string | null,
  // "profile_sidebar_fill_color": string | null,
  // "profile_text_color": string | null,
  // "profile_use_background_image": true,
  // "profile_image_url": string | null,
  // "profile_image_url_https": string | null,
  // "profile_banner_url": string | null,
  // "default_profile": true,
  // "default_profile_image": false,
  // "following": null,
  // "follow_request_sent": null,
  // "notifications": null,
  // "withheld_in_countries": [],
  "location_analyzed": {
    "in_english": string,
    "lang_detected": string,
    "latitude": number | null,
    "longitude": number | null,
    "country_name": string,
    "country_code": string,
  },
  "demographics": {
    "gender": GenderData,
    "age": AgeGroupData,
    "org": OrgData
  },
  "age_predicted": AgeGroupValue,
  "gender_predicted": GenderValue,
  "org_predicted": OrgValue,
}
