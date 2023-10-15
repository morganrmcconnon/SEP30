import re


def get_tweet_text(tweet):
    """
    Retrieve the text section of a tweet, considering extended tweets and text ranges.

    Use for Twitter API v1.1.

    Parameters:
    - tweet (dict): Twitter API v1 Object.

    Returns:
    - text (str).
    """
    if "extended_tweet" in tweet:
        extended_tweet = tweet["extended_tweet"]
        display_text_range = extended_tweet.get("display_text_range")
        if display_text_range and len(display_text_range) >= 2:
            return extended_tweet["full_text"][display_text_range[0]: display_text_range[1]]
        return extended_tweet["full_text"]
    display_text_range = tweet.get("display_text_range")
    if display_text_range and len(display_text_range) >= 2:
        return tweet["text"][display_text_range[0]: display_text_range[1]]
    return tweet["text"]



def clean_tweet_text(tweet_text):
    """
    Clean a tweet text.

    Parameters:
    - tweet_text (str): Tweet text to clean.

    Returns:
    - Cleaned tweet text (str).
    """
    # Remove RT, links, mentions, and other noise
    cleaned_text = re.sub(r'^RT[\s]+', '', tweet_text)  # Remove RT
    cleaned_text = re.sub(r'https?:\/\/\S+', '', cleaned_text)  # Remove links
    cleaned_text = re.sub(r'@[A-Za-z0-9]+', '', cleaned_text)  # Remove mentions
    cleaned_text = re.sub(r'#', '', cleaned_text)  # Remove hashtags

    return cleaned_text