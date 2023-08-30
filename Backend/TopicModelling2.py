import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string
import nltk
import json
import re

from nltk.stem import WordNetLemmatizer
from spacy.matcher import Matcher


documents = []
words = set(nltk.corpus.words.words())

file_path = "D:\Swinburne\S2 2023\Capstone\\testSM.json"  # Replace with the actual path to your file
with open(file_path, "r") as json_file:
    for line in json_file:
        text = (json.loads(line))["text"]
        text = re.sub('[^a-zA-Z0-9 \n\.]', ' ', text)
        text = text.replace("RT","")
        text = text.replace("http", "")
        #print(text)
        sent = text
        " ".join(w for w in nltk.wordpunct_tokenize(sent) \
                 if w.lower() in words or not w.isalpha())
        documents.append(sent.strip())


# Text preprocessing
def preprocess(text):
    return preprocess_string(text)

processed_documents = [preprocess(doc) for doc in documents]

# Create a dictionary and a corpus
dictionary = corpora.Dictionary(processed_documents)
corpus = [dictionary.doc2bow(doc) for doc in processed_documents]

# Train LDA model
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)


file_path = "D:\Swinburne\S2 2023\Capstone\keywords2.txt"  # Replace with the actual path to your file

keywords = set()

# Read keywords from the file
with open(file_path, "r") as keyword_file:
    for line in keyword_file:
        keywords.add(line.lower())

# Print topics and associated words
topics = lda_model.print_topics(num_words=5)

r = set()
for topic in topics:
    #print(topic[1])
    topicWords = topic[1].split('"')
    #print(topicWords)
    for i in range(1,len(topicWords),2):
        for tp in keywords:
            if topicWords[i] in tp:
                r.add(tp.replace("\n",""))
                break

print(r)
# Assign topics to documents
document_topics = [lda_model.get_document_topics(doc) for doc in corpus]
cnt = 0
for i in r:
    print(i)
    cnt += 1
    if cnt == 5: break