import { SentimentData, AgeGroupData, GenderData, OrgData } from "../data/api/types/constants";

export const SENTIMENT_KEY_MAP : SentimentData<string> = {
  'positive': 'Positive',
  'negative': 'Negative',
  'neutral': 'Neutral',
};

export const AGE_KEY_MAP : AgeGroupData<string> = {
  '<=18': 'Under 18',
  '19-29': '19-29',
  '30-39': '30-39',
  '>=40': 'Over 40',
};

export const GENDER_KEY_MAP : GenderData<string> = {
  'male': 'Male',
  'female': 'Female',
};

export const ORG_KEY_MAP : OrgData<string> = {
  'is-org': 'Organization',
  'non-org': 'Non-Organization',
};
