import { SentimentValue } from "./constants";
import { UserObject } from "./UserObject";


export type TweetObject = {
  id_str: string,
  timestamp_ms: string,
  text: string,
  text_in_english: string,
  user: UserObject,
  lang: string,
  sentiment: SentimentValue,
  spacy_match: {
    original: boolean,
    in_english: boolean,
  },
  text_processed: Array<string>,
  topic_bert_arxiv: {
    topic_id: number,
    topic_name: string,
  },
  topic_cardiffnlp: {
    topic_id: number,
    topic_name: string,
    topic_score: number
  },
  topic_lda: {
    model_id: string,
    topic_id: string,
    related_topics: {
      cosine_similarity: Array<string>,
      hellinger_distance: Array<string>,
    },
  }
};