import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the required data (run this only once)
nltk.download('vader_lexicon')

# Create a SentimentIntensityAnalyzer object
analyzer = SentimentIntensityAnalyzer()


def check_sentiment(text):
    # Analyze the sentiment of text
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']

    # Determine the sentiment label based on the compound score
    if compound_score >= 0.05:
        sentiment_label = 'Positive'
    elif compound_score <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return compound_score, sentiment_label