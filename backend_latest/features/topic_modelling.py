import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string
import nltk
import json
import re
from features import utils
#from features import clean_tweet_text
#from features import load_mental_health_keywords
from nltk.stem import WordNetLemmatizer
from spacy.matcher import Matcher

def clean_tweet_text(tweet_text):
    """
    Clean a tweet text.

    Parameters:
    - tweet_text (str): Tweet text to clean.

    Returns:
    - Cleaned tweet text (str).
    """
    # Remove RT, links, mentions, and other noise
    cleaned_text = re.sub(r'^RT[\s]+', '', tweet_text)  # Remove RT
    cleaned_text = re.sub(r'https?:\/\/\S+', '', cleaned_text)  # Remove links
    cleaned_text = re.sub(r'@[A-Za-z0-9]+', '', cleaned_text)  # Remove mentions
    cleaned_text = re.sub(r'#', '', cleaned_text)  # Remove hashtags

    return cleaned_text

def load_mental_health_keywords(file_path):
    keywords = set()

    # Read keywords from the file
    with open(file_path, "r") as keyword_file:
        for line in keyword_file:
            keywords.add(line.lower())

    #print(keywords)
    return keywords


def preprocess(text):
    return preprocess_string(text)


def process_topic_modelling(tweet_data):
    documents = []
    words = set(nltk.corpus.words.words())

    for tweet in tweet_data:
        tweet = clean_tweet_text(tweet)
        sent = tweet
        " ".join(w for w in nltk.wordpunct_tokenize(sent) \
                 if w.lower() in words or not w.isalpha())
        documents.append(sent.strip())

    # Text preprocessing
    processed_documents = [preprocess(doc) for doc in documents]

    # Create a dictionary and a corpus
    dictionary = corpora.Dictionary(processed_documents)
    corpus = [dictionary.doc2bow(doc) for doc in processed_documents]

    # Train LDA model
    lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

    # file_path = "data\keywords2.txt"  # Replace with the actual path to your file

    # keywords = load_mental_health_keywords(file_path)

    # Print topics and associated words
    topics = lda_model.print_topics(num_words=5)

    return topics


def define_topics(topics):
    r = set()

    file_path = "data\keywords2.txt"  # Replace with the actual path to your file

    keywords = load_mental_health_keywords(file_path)

    for topic in topics:
        # print(topic[1])
        topicWords = topic[1].split('"')
        # print(topicWords)
        for i in range(1, len(topicWords), 2):
            for tp in keywords:
                if topicWords[i] in tp:
                    r.add(tp.replace("\n", ""))
                    break

    return r


