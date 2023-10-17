# Download Tweets from Twitter Archive Dataset
The `download_tweets` folder within the components directory is dedicated to downloading tweets from the online Twitter Archive dataset. This dataset, provided freely and open-source, enables the Mental Health Dashboard project to access a vast collection of tweets for analysis.

## Modules

1. `download_tweets.py`

The `download_tweets.py` script is used to fetch tweets from the Twitter Archive dataset. By interacting with the dataset's API, this module retrieves the required tweet data for analysis and storage.

2. `get_download_url.py`

The `get_download_url.py` script is used to obtain the download URL for the Twitter Archive dataset. It generates the URL necessary for download_tweets.py to access and download the dataset.

## Initialization
The `__init__.py` file ensures that the download_tweets folder functions as a Python package, allowing seamless integration and utilization of its modules within the project.
