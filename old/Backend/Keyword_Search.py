import json

# Function to search for keyword in a tweet
def search_keyword_in_tweet(tweet, keyword):
    if 'text' in tweet and keyword.lower() in tweet['text'].lower():
        return True
    if 'extended_tweet' in tweet and 'full_text' in tweet['extended_tweet']:
        return keyword.lower() in tweet['extended_tweet']['full_text'].lower()
    return False

# Keyword to search for
keyword_to_search = "happy"

# Open the file and read JSON objects line by line
matching_tweets = []
with open('test.json', 'r', encoding='utf-8') as file:
    for line in file:
        tweet = json.loads(line)
        if search_keyword_in_tweet(tweet, keyword_to_search):
            matching_tweets.append(tweet)

# Print matching tweets
for tweet in matching_tweets:
    print("User:", tweet['user']['screen_name'])
    print("Date:", tweet['created_at'])
    if 'extended_tweet' in tweet and 'full_text' in tweet['extended_tweet']:
        print("Text:", tweet['extended_tweet']['full_text'])
    else:
        print("Text:", tweet['text'])
    print("-" * 50)
