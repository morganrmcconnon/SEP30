import { AgeGroupValue, GenderValue, OrgValue } from './constants';

export type UserObject = {
  id_str: string,
  country_name: string,
  country_code: string,
  age: AgeGroupValue,
  gender: GenderValue,
  org: OrgValue,
  lang: string,
}