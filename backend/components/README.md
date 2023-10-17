# Components Folder
The components folder in this project houses essential modules and scripts that form the backbone of the Mental Health Dashboard. Below is an overview of the folders and files contained within the components directory:

1. `__pycache__`
This folder contains Python bytecode compiled from the source files. It is generated automatically and is used to improve the startup time of the Python interpreter.

2. `analyze_tweets` Folder
The `analyze_tweets` folder contains scripts responsible for processing and analyzing raw tweet data. These scripts handle tasks such as sentiment analysis, topic modeling, and demographic analysis.

Files:
`define_topics.py`: Defines topics within the tweet dataset.
`detect_coordinates.py`: Detects geographical coordinates mentioned in tweets.
`detect_demographics.py`: Identifies demographic information from tweet content.
`detect_polygon_geojson.py`: Detects geographical polygons from tweet content.
`sentiment_analysis.py`: Performs sentiment analysis on tweets.
`sentiment_vader.py`: Utilizes the VADER sentiment analysis tool.
`spacy_matcher.py`: Matches keywords and entities in tweet text using spaCy.
`topic_bertopic_arxiv.py`: Applies BERTopic topic modeling to tweets.
`topic_cardiffnlp_tweet_topic.py`: Uses the CardiffNLP Tweet Topic model.
`topic_lda_load_pretrained.py`: Loads a pre-trained LDA topic model.
`topic_modelling.py`: Contains general functions for topic modeling.
`translate_text.py`: Translates tweet text to a specified language.
`tweet_text.py`: Extracts text content from raw tweets.

3. `data` Folder
The `data` separates code from data.

4. `download_tweets` Folder
The `download_tweets` folder contains scripts responsible for downloading tweets from an online Twitter Archive dataset.

Files:
`download_tweets.py`: Downloads tweets from the Twitter Archive dataset.
`get_download_url.py`: Retrieves the download URL for the Twitter Archive dataset.
`__init__.py`: Python package initializer.

5. `topic_model` Folder
The `topic_model` folder includes files related to topic modeling. Topic modeling identifies prevalent themes within collected tweets.

Files:
`lda_model.model`: Serialized LDA topic model.
`lda_model.model.expElogbeta.npy`: Topic-word distribution data for LDA model.
`lda_model.model.id2word`: Mapping of word IDs to words.
`lda_model.model.state`: State of the LDA model.
`topics.json`: Extracted topics with corresponding keywords.
6. `__init__.py`
This file is a Python package initializer. It defines what symbols the module exports when the package is imported.

7. `constants.py`
`constants.py` contains constant values used throughout the project. Constants provide meaningful names to values, enhancing the code's readability and maintainability.

8. `pipeline.py`
`pipeline.py` defines the main data processing pipeline for the Mental Health Dashboard project. It orchestrates the various components, ensuring data flows seamlessly through the system.

