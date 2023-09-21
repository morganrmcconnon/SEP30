from gensim import corpora
from gensim.models import LdaModel
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
def topic_modelling(texts: list[str], num_topics: int = NUM_TOPICS, save_to_file=None):
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
    topics_values = lda_model.show_topics(num_topics=num_topics, num_words=NUM_KEYWORDS_PER_TOPIC, formatted=False)
    topics_values = {
        topic_value[0]: [
            [keyword_value[0], float(keyword_value[1])] for keyword_value in topic_value[1]
        ]
        for topic_value in topics_values
    }

    return lda_model, topics_values


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
def apply_lda(text : str, lda_model : LdaModel):
    '''
    Apply the LDA model to detect the topics of a string of text
    
    :param `text`: the string of text to be processed
    :param `lda_model`: the trained LDA model
    '''
    processed_text = tokenize_lemmatize_and_remove_stopwords(text)
    bow = lda_model.id2word.doc2bow(processed_text)
    topics = lda_model.get_document_topics(bow)
    return topics
