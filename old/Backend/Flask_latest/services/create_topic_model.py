from analyze_tweets.topic_modelling import topic_modelling
from analyze_tweets.tweet_text import clean_tweet_text
import pandas as pd
import os
import json

data_path = os.path.join(os.path.dirname(__file__), "../data/Mental-Health-Twitter.csv")

# Load the data
df = pd.read_csv(data_path)
texts = df[df['label'] == 1]["post_text"]
texts = texts.transform(clean_tweet_text)
texts = texts.tolist()

model_directory = os.path.join(os.path.dirname(__file__), "topic_model")

# Create a directory to save the model
if not os.path.exists(model_directory):
    os.makedirs(model_directory, exist_ok=True)

# Create an LDA model
lda_model, topics = topic_modelling(texts, num_topics=5, save_to_file=os.path.join(model_directory, "lda_model.model"))

# Convert the probabilities from float32 to float for json serialization
topics_data = [[(topic_keywords_distribution[0], float(topic_keywords_distribution[1])) for topic_keywords_distribution in topic_keywords_distributions] for topic_keywords_distributions in topics]


with open(os.path.join(model_directory, "topics.json"), "w") as f:
    json.dump(topics_data, f)