import { TweetObject } from "./TweetObject";

export type BackendOutput = {
  aggregate_results: {
    total_tweets_count: number;
    related_tweets_count: number;
  };
  lda_topic_model: {
    keywords_representation: {
      [topic_id: string]: Array<[string, number]>,
    },
    labels: {
      [topic_id: string]: Array<{
        word: string,
        topic_id: number,
        topic_prob: number,
        topics: Array<[number, number]>
      }>;
    }
  }
  tweet_objects: TweetObject[];
};
