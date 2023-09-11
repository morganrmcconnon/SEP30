import json
import networkx as nx

# Load data from the JSON file
tweet_data = []
with open('test.json', 'r') as json_file:
    for line in json_file:
        tweet_data.append(json.loads(line))

# Create a directed graph using NetworkX
graph = nx.DiGraph()

# Iterate through the data and add nodes and edges
for tweet in tweet_data:
    if 'text' in tweet and 'user' in tweet:
        text = tweet['text'].lower()
        user = tweet['user']['screen_name']

        if 'happy' in text or 'sad' in text:  # Search for both keywords
            graph.add_node(user, label=user, color='blue' if 'happy' in text else 'red')  # Adding label and color
            mentions = []
            if 'entities' in tweet and 'user_mentions' in tweet['entities']:
                mentions = [mention['screen_name'] for mention in tweet['entities']['user_mentions']]
            
            for mention in mentions:
                graph.add_node(mention, label=mention, color='blue' if 'happy' in text else 'red')  # Adding label and color
                graph.add_edge(user, mention)

# Export the graph in GEXF format for Gephi
nx.write_gexf(graph, 'gephi_graph_with_keywords.gexf')
print("Graph exported to gephi_graph_with_keywords.gexf")
