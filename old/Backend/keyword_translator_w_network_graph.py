
##**Install Packages**
"""

pip install googletrans

"""
##**Translator and Graph**"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from googletrans import Translator, LANGUAGES

# Function to search for a keyword in a tweet
def search_keyword_in_tweet(tweet, keyword):
    if 'text' in tweet and keyword.lower() in tweet['text'].lower():
        return True
    if 'extended_tweet' in tweet and 'full_text' in tweet['extended_tweet']:
        return keyword.lower() in tweet['extended_tweet']['full_text'].lower()
    return False

# Function to translate non-English tweets to English
def translate_tweet(tweet):
    if 'text' in tweet and tweet['lang'] != 'en':
        try:
            translator = Translator()
            translation = translator.translate(tweet['text'], dest='en')
            tweet['text'] = translation.text
        except Exception as e:
            print(f"Translation error: {str(e)}")

# Keyword to search for
keyword_to_search = "happy"

# Open the file and read JSON objects line by line
matching_tweets = []
with open('test.json', 'r', encoding='utf-8') as file:
    for line in file:
        tweet = json.loads(line)
        if search_keyword_in_tweet(tweet, keyword_to_search):
            if tweet['lang'] != 'en':
                translate_tweet(tweet)
            matching_tweets.append(tweet)

# Create a directed graph
G = nx.DiGraph()

# Add nodes (tweets) and edges (language)
for tweet in matching_tweets:
    tweet_id = tweet['id_str']
    user_screen_name = tweet['user']['screen_name']
    language = tweet['lang']

    G.add_node(tweet_id, user=user_screen_name)
    G.add_node(language, language=True, label=LANGUAGES.get(language, language))

    G.add_edge(tweet_id, language)

# Plot the network graph with labels for language nodes
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42)

# Get labels for language nodes
language_labels = {node: data['label'] for node, data in G.nodes(data=True) if data.get('language', False)}

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_size=30, node_color='green')
nx.draw_networkx_edges(G, pos, arrows=False)
nx.draw_networkx_labels(G, pos, labels=language_labels, font_size=20, font_color='purple')

plt.title(f"Language Network Graph for '{keyword_to_search}' (Translated to English)")
plt.show()