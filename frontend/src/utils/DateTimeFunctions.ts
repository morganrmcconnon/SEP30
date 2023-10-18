export function timestampToShortDayMonth(timestamp: string): string {
  const parsedTimestamp = parseInt(timestamp, 10); // Parse the string timestamp into a number
  return timestampIntToShortDayMonth(parsedTimestamp);
}

export function timestampIntToShortDayMonth(timestamp: number): string {
  const date = new Date(timestamp);
  const options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' };
  return date.toLocaleDateString(undefined, options);
}

export function timestampToDayTimestamp(timestamp: number) : number {
  const date = new Date(timestamp);
  date.setUTCHours(0, 0, 0, 0);
  return date.getTime();
}