from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer


# Preprocessing: tokenization, stopword removal, and lemmatization
def preprocess(text):
    '''
    Preprocess a string of text by tokenizing, removing stopwords, and lemmatizing.
    '''
    lemmatizer = WordNetLemmatizer()
    result = []
    for token in simple_preprocess(text): # Tokenize the text
        if token not in STOPWORDS and len(token) > 2: # Remove stopwords and tokens with length less than 3
            result.append(lemmatizer.lemmatize(token)) # Lemmatize the token and add it to the result
    return result


#  Create an lda model from a set of texts
def topic_modelling(texts : list[str], num_topics : int = 10, save_to_file = None):
    '''
    Create an lda topic model from a set of texts
    :param `texts`: a list of strings
    :param `num_topics`: the number of topics to be extracted
    :param `save_to_file`: the file to save the trained model to, e.g. "lda_model.model"

    Returns the trained LDA model
    '''

    processed_texts = [preprocess(text) for text in texts]

    # Create a dictionary and a corpus
    dictionary = corpora.Dictionary(processed_texts)
    corpus = [dictionary.doc2bow(tweet) for tweet in processed_texts]

    # Train the LDA model
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    if save_to_file:
        # Save the trained model
        lda_model.save(save_to_file)
        print(f"LDA model saved to {save_to_file}")

    return lda_model


# Extract keywords and probability distributions from the LDA model
def extract_keywords_probability_distribution(lda_model, num_topics : int = 10):
    '''
    Extract keywords and probability distributions from the LDA model
    
    :param `lda_model`: the trained LDA model
    :param `num_topics`: the number of topics to be extracted

    Returns a list of dictionaries, each dictionary contains the keywords and probability distribution of a topic

    '''
    topics_data = []
    for topic_id in range(num_topics):
        topic_keywords = lda_model.show_topic(topic_id)
        topic_data = {
            "keywords": [keyword for keyword, _ in topic_keywords],
            "probabilities": [probability for _, probability in topic_keywords]
        }
        topics_data.append(topic_data)
    return topics_data


# Load the saved LDA model
def load_model(model_file):
    '''
    Load the saved LDA model

    :param `model_file`: the file to load the model from, e.g. "lda_model.model"

    Returns the trained LDA model

    '''
    lda_model = LdaModel.load(model_file)
    return lda_model


# Function to apply LDA model to detect the topics of a string of text
def apply_lda(text, lda_model):
    '''
    Apply the LDA model to detect the topics of a string of text
    
    :param `text`: the string of text to be processed
    :param `lda_model`: the trained LDA model
    '''
    processed_text = preprocess(text)
    bow = lda_model.id2word.doc2bow(processed_text)
    topics = lda_model.get_document_topics(bow)
    return topics