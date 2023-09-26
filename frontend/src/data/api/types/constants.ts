export type AgeGroupValue = "<=18" | "19-29" | "30-39" | ">=40";

export type GenderValue = "male" | "female";

export type OrgValue = "is-org" | "non-org";

export type SentimentValue = "negative" | "neutral" | "positive";

export type AgeGroupData = Record<AgeGroupValue, number>;

export type GenderData = Record<GenderValue, number>;

export type OrgData = Record<OrgValue, number>;

export type SentimentData = { [value in SentimentValue] : number};