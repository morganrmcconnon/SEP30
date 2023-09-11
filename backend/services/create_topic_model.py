from analyze_tweets.topic_modelling import topic_modelling
from analyze_tweets.tweet_text import clean_tweet_text
import pandas as pd
import os
import json

current_dir = os.path.dirname(__file__)
training_data_path = os.path.join(current_dir, "data/Mental-Health-Twitter.csv")
model_folder_path = os.path.join(current_dir, "topic_model")
save_model_to_file = os.path.join(model_folder_path, "lda_model.model")
save_topics_to_file = os.path.join(model_folder_path, "topics.json")


# Load the training data
df = pd.read_csv(training_data_path)
texts = df[df['label'] == 1]["post_text"]
texts = texts.transform(clean_tweet_text)
texts = texts.tolist()


# Create a directory to save the model
if not os.path.exists(model_folder_path):
    os.makedirs(model_folder_path, exist_ok=True)

# Create an LDA model
lda_model, topics = topic_modelling(texts, num_topics=5, save_to_file=save_model_to_file)

# Convert the probabilities from float32 to float for json serialization
topics_data = [[(topic_keywords_distribution[0], float(topic_keywords_distribution[1])) for topic_keywords_distribution in topic_keywords_distributions] for topic_keywords_distributions in topics]

# Save the topics to a json file
with open(save_topics_to_file, "w") as f:
    json.dump(topics_data, f)