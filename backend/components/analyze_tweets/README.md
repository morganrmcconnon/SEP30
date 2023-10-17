# Analyze Tweets
The `analyze_tweets` folder within the components directory houses essential modules for tweet analysis in the Mental Health Dashboard project. `These modules are responsible for various tasks such as topic modeling, sentiment analysis, geographic data processing, and demographic analysis.

## Modules
1. `define_topics.py`

This module defines topics based on tweet content.

2. `detect_coordinates.py`

Detects geographic coordinates mentioned in tweets. Geolocation data is used for mapping mental health discussions across different regions.

3. `detect_demographics.py`

Analyzes tweets to identify demographic information such as age groups, gender, and other relevant data. Demographic analysis provides insights into the specific demographics discussing mental health topics.

4. `detect_polygon_geojson.py`

Detects polygons from geographic coordinates. `This module is used for mapping mental health discussions accurately on a geographical map.

5. `sentiment_analysis.py`

Performs sentiment analysis on tweets to determine the emotional tone of the content. 

6. `sentiment_vader.py`

Uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis tool to assess the sentiment of tweets. VADER is specifically designed for social media text.

7. `spacy_matcher.py`

Utilizes spaCy's natural language processing capabilities to perform text matching, enabling the identification of specific patterns or entities within tweets.

8. `topic_bertopic_arxiv.py`

Applies BERTopic, a topic modeling technique based on transformer models, to identify topics present in mental health-related tweets.

9. `topic_cardiffnlp_tweet_topic.py`

Utilizes the CardiffNLP Tweet Topic Model to identify topics in tweets. This module provides an alternative approach to topic modeling.

10. `topic_lda_load_pretrained.py`

Applies Latent Dirichlet Allocation (LDA) topic modeling to tweets using a pre-trained model. LDA is a widely used technique for topic modeling, providing coherent topics from tweet data.

11. `topic_modelling.py`

Performs topic modeling on tweets to identify prevalent themes and subjects in mental health-related discussions. 

12. `translate_text.py`

Translates tweets from one language to another, enabling multilingual analysis. 

13. `tweet_text.py`

Processes raw tweet text, including tokenization and cleaning. 

## Contact
For any inquiries or issues related to the functionality of these modules, please contact us at twittermentalhealth30@gmail.com.

Thank you for your contributions to the tweet analysis components of the Mental Health Dashboard! Your efforts are invaluable in ensuring the accuracy and depth of our data analysis processes.