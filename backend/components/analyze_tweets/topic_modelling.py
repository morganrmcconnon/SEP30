import os

from gensim import corpora
from gensim.models import LdaModel
from gensim.models.ldamodel import LdaModel
from gensim.matutils import cossim, hellinger
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

# The number of topics to be extracted
NUM_TOPICS = 10
# Number of the most significant words that are associated with the topic.
NUM_KEYWORDS_PER_TOPIC = 100


# Preprocessing: tokenization, stopword removal, and lemmatization
def tokenize_lemmatize_and_remove_stopwords(text):
    '''
    Preprocess a string of text by tokenizing, removing stopwords, and lemmatizing.
    
    Stopwords are words that are too common and do not contribute to the meaning of the text, e.g. "the", "a", "an", "is", "are", etc.
    
    Lemmatization is the process of converting a word to its base form, e.g. "dogs" to "dog", "wolves" to "wolf", etc.

    Tokenization is the process of splitting a string of text into a list of tokens, e.g. "I love dogs and cats" to ["I", "love", "dogs", "and", "cats"]
    '''
    lemmatizer = WordNetLemmatizer()
    result = []
    for token in simple_preprocess(text):  # Tokenize the text
        if token not in STOPWORDS and len(token) > 2:  # Remove stopwords and tokens with length less than 3
            result.append(lemmatizer.lemmatize(token))  # Lemmatize the token and add it to the result
    return result


#  Create an lda model from a set of texts
def create_topic_model(texts: list[str], num_topics: int = NUM_TOPICS, save_to_file=None):
    '''
    Create an lda topic model from a set of texts
    :param `texts`: a list of strings
    :param `num_topics`: the number of topics to be extracted
    :param `save_to_file`: the file to save the trained model to, e.g. "lda_model.model"

    Returns the trained LDA model, and a list of lists, each list contains the keywords and probability distribution of a topic
    '''

    processed_texts = [tokenize_lemmatize_and_remove_stopwords(text) for text in texts]

    # Create a dictionary and a corpus
    dictionary = corpora.Dictionary(processed_texts)
    corpus = [dictionary.doc2bow(text) for text in processed_texts]

    # Train the LDA model
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    if save_to_file:
        # Save the trained model
        lda_model.save(save_to_file)
        print(f"LDA model saved to {save_to_file}")

    # Get the keywords and probability distribution of each topic
    topics_keywords_representations = lda_model.show_topics(num_topics=num_topics, num_words=NUM_KEYWORDS_PER_TOPIC, formatted=False)
    # Serialize into floats
    for topic_topics_keywords_representation in topics_keywords_representations:
        for keyword_value in topic_topics_keywords_representation[1]:
            keyword_value[1] = float(keyword_value[1])
    return lda_model, topics_keywords_representations


# Load the saved LDA model
def load_model(model_file):
    '''
    Load the saved LDA model

    :param `model_file`: the file to load the model from, e.g. "lda_model.model"

    Returns the trained LDA model

    '''
    lda_model : LdaModel = LdaModel.load(model_file)
    return lda_model


# Function to apply LDA model to detect the topics of a string of text
def apply_lda_model(text : str, lda_model : LdaModel):
    '''
    Apply the LDA model to detect the topics probability distributions of a text
    
    :param `text`: the string of text to be processed
    :param `lda_model`: the trained LDA model

    Returns a list of tuples, each tuple contains the topic id and the probability of the topic, e.g. [(0, 0.1), (1, 0.2), (2, 0.3), (3, 0.4)]
    '''
    processed_text = tokenize_lemmatize_and_remove_stopwords(text)
    bow = lda_model.id2word.doc2bow(processed_text)
    topics_distribution = lda_model.get_document_topics(bow)
    topics_distribution = [[topic[0], float(topic[1])] for topic in topics_distribution]
    topics_distribution.sort(key=lambda x: x[0])
    return topics_distribution



# Function to get the keywords of a topic model
def get_keywords_of_topic_model(lda_topics_representations):
    '''
    Get the keywords of a topic model

    :param `lda_topics_representations`: a list of lists, each list contains the keywords and probability distribution of a topic

    Returns a dictionary, each key is the topic id, and each value is a list of keywords of the topic
    '''
    keywords_of_topic_model = {}
    for topic_id, topic_representation in lda_topics_representations.items():
        keywords_of_topic_model[topic_id] = []
        for keyword, prob in topic_representation:
            if keyword not in keywords_of_topic_model:
                keywords_of_topic_model[topic_id].append(keyword)
    return keywords_of_topic_model

#TLL
current_dir = os.path.dirname(os.path.realpath(__file__))
keywords2_file_path = os.path.join(current_dir, "../data/keywords2.txt")

KEYWORDS2_LIST = []
with open(keywords2_file_path) as f:
    for line in f:
        KEYWORDS2_LIST.append(line.strip())

def get_topics_distributions(lda_model: LdaModel, labels_list: list[str] = KEYWORDS2_LIST) -> list[
    str, list[int, list]]:
    topics_distributions_list = []
    # Get unique labels
    labels_list = list(set(labels_list))
    for word in labels_list:
        topics_distributions = apply_lda_model(word, lda_model)
        topics_distributions_list.append([word, topics_distributions])
    return topics_distributions_list


def get_similarity_score(topics_distribution_list_1: list, topics_distribution_list_2: list, method="cossim"):
    if method == "cossim":
        return cossim(topics_distribution_list_1, topics_distribution_list_2)
    else:  # method == "hellinger":
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


def get_similarity_scores(labels_topics_distributions_list: list[str, list[int, list]],
                          topics_distribution: list[int, list], method="cossim") -> list[str, float]:
    similarity_scores = []
    for item in labels_topics_distributions_list:
        label = item[0]
        label_topics_distribution = item[1]
        similarity_scores.append([label, get_similarity_score(label_topics_distribution, topics_distribution, method)])
    return similarity_scores