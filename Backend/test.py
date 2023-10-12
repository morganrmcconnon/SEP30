import requests
import tweepy
import logging
import json

# Twitter API credentials
TWITTER_API_KEY = '_TWITTER_API_KEY'
TWITTER_API_SECRET = '_TWITTER_API_SECRET'
TWITTER_ACCESS_TOKEN = '_TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = '_TWITTER_ACCESS_TOKEN_SECRET'

# Backend API endpoint for the mental health dashboard
BACKEND_API_URL = 'BACKEND_API_URL'

# Setup logging
logging.basicConfig(filename='dashboard_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to authenticate with Twitter API
def authenticate_twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

# Function to fetch Twitter data based on a keyword
def fetch_twitter_data(api, keyword, count=10):
    try:
        tweets = tweepy.Cursor(api.search, q=keyword, count=count, lang='en').items(count)
        twitter_data = []
        for tweet in tweets:
            twitter_data.append(tweet._json)
        return twitter_data
    except Exception as e:
        logging.error(f'Error fetching Twitter data: {str(e)}')
        return None

# Function to send data to the backend API endpoint
def send_data_to_backend(data):
    try:
        response = requests.post(f'{BACKEND_API_URL}/mental-health-data', json=data)
        response.raise_for_status()
        logging.info('Data sent to backend successfully.')
        return response.json()
    except requests.exceptions.HTTPError as errh:
        logging.error(f'HTTP Error: {errh}')
    except requests.exceptions.ConnectionError as errc:
        logging.error(f'Error Connecting: {errc}')
    except requests.exceptions.Timeout as errt:
        logging.error(f'Timeout Error: {errt}')
    except requests.exceptions.RequestException as err:
        logging.error(f'Request Exception: {err}')



# Translate tweets using Google Translate API
def translate_tweets(tweets):
    try:
        translator = Translator()
        translated_tweets = [translator.translate(tweet, dest='en').text for tweet in tweets]
        return translated_tweets
    except Exception as e:
        print(f'Error translating tweets: {str(e)}')
        return None

# Perform sentiment analysis using TextBlob
def analyze_sentiment(tweets):
    sentiments = []
    try:
        for tweet in tweets:
            analysis = TextBlob(tweet)
            sentiment = 'Positive' if analysis.sentiment.polarity > 0 else 'Negative' if analysis.sentiment.polarity < 0 else 'Neutral'
            sentiments.append(sentiment)
        return sentiments
    except Exception as e:
        print(f'Error analyzing sentiment: {str(e)}')
        return None

# Perform demographic analysis using SpaCy (example: extracting named entities)
def analyze_demographics(tweets):
    try:
        nlp = spacy.load('en_core_web_sm')
        entities = []
        for tweet in tweets:
            doc = nlp(tweet)
            for entity in doc.ents:
                entities.append(entity.text)
        return entities
    except Exception as e:
        print(f'Error analyzing demographics: {str(e)}')
        return None





# Main function
def main():
    try:
        # Authenticate with Twitter API
        twitter_api = authenticate_twitter_api()

        # Fetch Twitter data based on the keyword
        twitter_keyword = 'mental health'
        twitter_data = fetch_twitter_data(twitter_api, twitter_keyword, count=10)

        if twitter_data:
            # Send Twitter data to the backend API
            backend_response = send_data_to_backend(twitter_data)
            if backend_response:
                print('Data sent to the backend successfully.')
        else:
            print('Error fetching Twitter data. Please check the logs for more details.')
    
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        print(f'An error occurred. Please check the logs for more details: {str(e)}')


try:
        # Authenticate with Twitter API
        twitter_api = authenticate_twitter_api()

        # Fetch Twitter data based on the keyword
        twitter_keyword = 'mental health'
        twitter_data = fetch_twitter_data(twitter_api, twitter_keyword, count=10)

        if twitter_data:
            # Translate tweets to English
            translated_tweets = translate_tweets(twitter_data)

            # Perform sentiment analysis
            sentiments = analyze_sentiment(translated_tweets)

            # Perform demographic analysis
            demographics = analyze_demographics(translated_tweets)

            # Print the results
            print('Original Tweets:', twitter_data)
            print('Translated Tweets:', translated_tweets)
            print('Sentiments:', sentiments)
            print('Demographics:', demographics)
        else:
            print('Error fetching Twitter data. Please check the logs for more details.')
    
    except Exception as e:
        print(f'An error occurred: {str(e)}')

if __name__ == "__main__":
    main()
