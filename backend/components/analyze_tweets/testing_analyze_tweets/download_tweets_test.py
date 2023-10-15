import unittest
from unittest.mock import patch, Mock
from ..download_tweets import download_tweets
class TestDownloadTweets(unittest.TestCase):

    def test_download_tweets_bz2(self):
        # Test downloading and extracting tweets from a BZIP2-compressed JSONL file
        url = "https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-09.zip/2011%2F09%2F27%2F20%2F35.json.bz2"  # .bz2 file download link
        data = download_tweets(url)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        print("Downloaded data from .bz2 file:")
        #line_length = 20
        for i in range(0, len(data), 1):
            print(data[i:i+1])
        print()

    def test_download_tweets_gz(self):
        # Test downloading and extracting tweets from a GZIP-compressed JSONL file
        url = "https://archive.org/download/archiveteam-twitter-stream-2022-08/twitter-stream-20220804.tar/20220804%2F20220804000400.json.gz"  # .gz file download link
        data = download_tweets(url)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        print("Downloaded data from .gz file:")
        #line_length = 20
        for i in range(0, len(data), 1):
            print(data[i:i+1])
        print()

        print()
    def test_download_tweets_invalid_format(self):
        # Test downloading from an unsupported file format (should result in a ValueError)
        url = "https://archive.org/download/archiveteam-twitter-stream-2022-09/twitter-stream-20220902.tar"  #Invalid URL
        data = download_tweets(url)
        self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
