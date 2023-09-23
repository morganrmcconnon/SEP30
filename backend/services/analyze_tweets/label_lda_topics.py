import os
from gensim.models.ldamodel import LdaModel

from .topic_modelling import apply_lda
from .load_pretrained_topic_model import load_pretrained_model

current_dir = os.path.dirname(os.path.realpath(__file__))
keywords2_file_path = os.path.join(current_dir, "../data/keywords2.txt")

KEYWORDS2_LIST = []
with open(keywords2_file_path) as f:
    for line in f:
        KEYWORDS2_LIST.append(line.strip())

def label_lda_topics(lda_model: LdaModel, labels_list: list) -> dict:
    topics_count = lda_model.num_topics
    topics_label = { i: [] for i in range(topics_count) }
    for word in labels_list:
        topics = apply_lda(word, lda_model)
        topic_highest_value = max(topics, key=lambda x: x[1])
        topic_id = topic_highest_value[0]
        topic_prob = topic_highest_value[1]
        # Serialize the probability values
        topics = [[topic[0], float(topic[1])] for topic in topics]
        obj = {
            "word": word,
            "topic_id": topic_id,
            "topic_prob": topic_prob,
            "topics": topics
        }
        if topic_id not in topics_label:
            topics_label[topic_id] = [obj]
        else:
            topics_label[topic_id].append(obj)

    return topics_label

def label_topics_from_preexisting_keywords_list(lda_model: LdaModel) -> dict:
    return label_lda_topics(lda_model, KEYWORDS2_LIST)

def label_topics_from_preexisting_topic_model_and_keywords_list() -> dict:
    lda_model = load_pretrained_model()
    return label_lda_topics(lda_model, KEYWORDS2_LIST)