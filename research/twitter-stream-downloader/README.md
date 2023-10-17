# Twitter Stream Downloader

A research on how to download tweets from Twitter Stream Collection from the Internet Archive: https://archive.org/details/twitterstream

The result of this research are Python files that can be used to download tweets from the Twitter Stream Collection: `download_tweets.py` and `get_download_url.py`.

In this research, we scrape the Twitter Stream Collection page to get the download URLs of the Twitter Stream Collection. Then, we use the download URLs to download the Twitter Stream Collection. The urls are saved in a folder called `urls`.

However, having to use this folder as part of the downloader program will be inconvenient. Therefore, we tried to recognize the pattern of the download URLs and use the pattern to generate the download URLs. The result is the `get_download_url.py` file.

All scripts used in this research are in the `scripts` folder.

The source of this repository is available at: https://github.com/thanhan910/twitter-stream-downloader