import json
import re


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


def read_jsonl(local_path):
    """
    Read a JSONL file.

    Parameters:
    - local_path (str): Path to the JSONL file.

    Returns:
    - A list of dictionaries.
    """
    with open(local_path, "r") as f:
        return [json.loads(line) for line in f]


def get_tweet_text(tweet):
    """ 
    Retrieve the text section of a tweet, considering extended tweets and text ranges.

    Parameters:
    - tweet (dict): Twitter API v1 Object.

    Returns:
    - text (str).
    """
    if "extended_tweet" in tweet:
        extended_tweet = tweet["extended_tweet"]
        display_text_range = extended_tweet.get("display_text_range")
        if display_text_range and len(display_text_range) >= 2:
            return extended_tweet["full_text"][
                display_text_range[0] : display_text_range[1]
            ]
        return extended_tweet["full_text"]
    display_text_range = tweet.get("display_text_range")
    if display_text_range and len(display_text_range) >= 2:
        return tweet["text"][display_text_range[0] : display_text_range[1]]
    return tweet["text"]


def remove_none_entries(list_of_dicts, inplace=True):
    """
    Remove keys with None values from each dictionary in the list.

    Parameters:
    - list_of_dicts (list of dict): List of dictionaries to process.
    - inplace (bool): If True, modify the input list in-place. If False, return a modified copy.

    Returns:
    - None if inplace=True, otherwise a modified list of dictionaries.
    """
    if inplace:
        for d in list_of_dicts:
            # Find keys with None values
            keys_to_remove = [key for key, value in d.items() if value is None]
            # Remove keys with None values
            for key in keys_to_remove:
                del d[key]
    else:
        # Create a new list of dictionaries
        new_list = [dict(d) for d in list_of_dicts]
        for d in new_list:
            # Create a new dictionary with keys filtered
            d = {key: value for key, value in d.items() if value is not None}
        return new_list


def complete_dict_entries(list_of_dicts, inplace=True):
    """
    Complete missing keys with None values in each dictionary.

    Parameters:
    - list_of_dicts (list of dict): List of dictionaries to process.
    - inplace (bool): If True, modify the input list in-place. If False, return a modified copy.

    Returns:
    - None if inplace=True, otherwise a modified list of dictionaries.
    """
    all_keys = set()
    for d in list_of_dicts:
        all_keys.update(d.keys())

    if inplace:
        for d in list_of_dicts:
            # Complete missing keys with None values
            for key in all_keys:
                if key not in d:
                    d[key] = None
    else:
        # Create a new list of dictionaries
        new_list = [dict(d) for d in list_of_dicts]
        for d in new_list:
            # Complete missing keys with None values
            for key in all_keys:
                if key not in d:
                    d[key] = None
        return new_list


def shared_keys(dicts):
    """
    Given a list of dictionaries, return the keys that occur in all dictionaries, and all other keys.
    """
    if not dicts:
        return []

    # Create a dictionary to store key counts
    key_counts = {}

    # Count the occurrence of keys in each dictionary
    for d in dicts:
        for key in d.keys():
            key_counts[key] = key_counts.get(key, 0) + 1

    # Filter keys that occur in all dictionaries
    common_keys = [key for key, count in key_counts.items() if count == len(dicts)]
    non_common_keys = [key for key, count in key_counts.items() if count != len(dicts)]

    return common_keys, non_common_keys
