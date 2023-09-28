import os
from gensim.models.ldamodel import LdaModel
from gensim.matutils import cossim, hellinger

from .topic_modelling import apply_lda_model
from .topic_lda_load_pretrained import load_pretrained_model

current_dir = os.path.dirname(os.path.realpath(__file__))
keywords2_file_path = os.path.join(current_dir, "../data/keywords2.txt")

KEYWORDS2_LIST = []
with open(keywords2_file_path) as f:
    for line in f:
        KEYWORDS2_LIST.append(line.strip())

def get_topics_distributions(lda_model: LdaModel, labels_list : list[str] = KEYWORDS2_LIST) -> list[str, list[int, list]]:
    topics_distributions_list = []
    # Get unique labels
    labels_list = list(set(labels_list))
    for word in labels_list:
        topics_distributions = apply_lda_model(word, lda_model)
        topics_distributions_list.append([word, topics_distributions])
    return topics_distributions_list

def get_similarity_score(topics_distribution_list_1 : list, topics_distribution_list_2 : list, method ="cossim"):
    if method == "cossim":
        return cossim(topics_distribution_list_1, topics_distribution_list_2)
    else: # method == "hellinger":
        # In case 2 vectors have different length
        topics_map_1 = {item[0]: item[1] for item in topics_distribution_list_1}
        topics_map_2 = {item[0]: item[1] for item in topics_distribution_list_2}
        for topic in topics_map_2:
            if topic not in topics_map_1:
                topics_map_1[topic] = 0
        for topic in topics_map_1:
            if topic not in topics_map_2:
                topics_map_2[topic] = 0
        topics_map = {}
        for topic in topics_map_1:
            topics_map[topic] = [topics_map_1[topic], topics_map_2[topic]]
        
        topics_vector_1 = [item[1][0] for item in sorted(topics_map.items(), key=lambda item: item[0])]
        topics_vector_2 = [item[1][1] for item in sorted(topics_map.items(), key=lambda item: item[0])]

        return hellinger(topics_vector_1, topics_vector_2)
    

def get_similarity_scores(labels_topics_distributions_list : list[str, list[int, list]], topics_distribution: list[int, list], method="cossim") -> list[str, float]:
    similarity_scores = []
    for item in labels_topics_distributions_list:
        label = item[0]
        label_topics_distribution = item[1]
        similarity_scores.append([label, get_similarity_score(label_topics_distribution, topics_distribution, method)])
    return similarity_scores