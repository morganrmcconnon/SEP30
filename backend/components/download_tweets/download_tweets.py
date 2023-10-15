import json
import bz2
import gzip
from urllib.request import urlopen

def download_tweets(url):
    '''
    Downloads and extracts data from a compressed jsonl file on the Internet Archive Twitter Stream collection.
    '''
    try:
        with urlopen(url) as response:
            if url.endswith('.json.bz2'):
                with bz2.open(response, 'rt', encoding='utf-8') as file:
                    data = [json.loads(line) for line in file.readlines()]
            elif url.endswith('.json.gz'):
                with gzip.open(response, 'rt', encoding='utf-8') as file:
                    data = [json.loads(line) for line in file.readlines()]
            else:
                raise ValueError("Unsupported file format. Only .json.bz2 and .json.gz are supported.")

        return data

    except Exception as e:
        print(f"Error: {e}")
        return None
