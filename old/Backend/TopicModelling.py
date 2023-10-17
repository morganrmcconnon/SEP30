import gensim
from gensim import corpora
from nltk.tokenize import word_tokenize

# Preprocessed text
preprocessed_text = "This is an example sentence for topic modeling."

# Tokenize the text using NLTK
tokenized_text = word_tokenize(preprocessed_text)

# Create a dictionary mapping words to IDs
dictionary = corpora.Dictionary([tokenized_text])

# Convert the tokenized text into a bag-of-words representation
corpus = [dictionary.doc2bow(tokenized_text)]


# Train the LDA model
lda_model = gensim.models.ldamodel.LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=5,  # Choose the number of topics
    passes=10
)

# Print the top words for each topic
topics = lda_model.print_topics(num_words=10)
for topic in topics:
    print(topic)
