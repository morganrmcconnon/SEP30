from bertopic import BERTopic

BERTOPIC_ARXIV_TOPIC_MODEL = BERTopic.load("MaartenGr/BERTopic_ArXiv")


def detect_topics_bertopic_arxiv(texts: list[str]):
    """
    Detects the topic of a tweet using BERTopic trained on ArXiv.
    """
    topics_detected_list, probs_detected_list = BERTOPIC_ARXIV_TOPIC_MODEL.transform(texts)
    return topics_detected_list, probs_detected_list

def get_topic_info_bertopic_arxiv(topic_id: int):
    """
    Returns the topic info from the BERTopic model trained on ArXiv.
    """
    return BERTOPIC_ARXIV_TOPIC_MODEL.get_topic_info(topic_id).to_dict(orient="records")

def find_topics_bertopic_arxiv(search_term: str):
    """
    Find topics most similar to a search_term.
    """
    return BERTOPIC_ARXIV_TOPIC_MODEL.find_topics(search_term)
