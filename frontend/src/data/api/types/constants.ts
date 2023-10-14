export type AgeGroupValue = "<=18" | "19-29" | "30-39" | ">=40";

export type GenderValue = "male" | "female";

export type OrgValue = "is-org" | "non-org";

export type SentimentValue = "negative" | "neutral" | "positive";

export type AgeGroupData<T> = Record<AgeGroupValue, T>;

export type GenderData<T> = Record<GenderValue, T>;

export type OrgData<T> = Record<OrgValue, T>;

export type SentimentData<T> = { [value in SentimentValue] : T};