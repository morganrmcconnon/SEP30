
import unittest
from tweet_text import get_tweet_text, clean_tweet_text

class TestTweetText(unittest.TestCase):

    #Get tweet text test
    def test_get_tweet_text_extended(self):
        # Test a tweet with extended tweet
        tweet = {
            "extended_tweet": {
                "full_text": "This is an extended tweet.",
                "display_text_range": [0, 25] 
            }
        }
        expected_text = "This is an extended tweet"
        print("Tweet w/ Extended Tweet:", get_tweet_text(tweet))
        print("Expected Text:", expected_text)
        self.assertEqual(get_tweet_text(tweet), expected_text)

    def test_get_tweet_text_Not_Extended(self):
          # Test a tweet without extended tweet
        tweet = {
            "text": "This is a normal tweet."
        }
        expected_text = "This is a normal tweet."
        print("Tweet w/o Extended Tweet:", get_tweet_text(tweet) )
        print("Expected Text:", expected_text)
        self.assertEqual(get_tweet_text(tweet), expected_text)
  
  
    #Cleaning text test
    def test_clean_tweet_text_RT(self):
        # Test cleaning a tweet with various elements
        tweet_text = "RT pls help me get the concert tickets!"
        print("Cleaned Text (RT):", clean_tweet_text(tweet_text))
        expected_cleaned_text = "pls help me get the concert tickets!"
        print("Expected Cleaned Text:", expected_cleaned_text)
        self.assertEqual(clean_tweet_text(tweet_text), expected_cleaned_text)


    def test_clean_tweet_text_Links(self):
        # Test cleaning a tweet with various elements
        tweet_text = "Check out this link https://example.com, pretty nifty."
        print("Cleaned Text (Links):", clean_tweet_text(tweet_text))
        expected_cleaned_text = "Check out this link  , pretty nifty."
        print("Expected Cleaned Text:", expected_cleaned_text)
        self.assertEqual(clean_tweet_text(tweet_text), expected_cleaned_text)


    def test_clean_tweet_text_Mentions(self):
        # Test cleaning a tweet with various elements
        tweet_text = "@user123 I know where you live."
        print("Cleaned Text (Mentions):", clean_tweet_text(tweet_text))
        expected_cleaned_text = "I know where you live."
        print("Expected Cleaned Text:", expected_cleaned_text)
        self.assertEqual(clean_tweet_text(tweet_text), expected_cleaned_text)


    def test_clean_tweet_text_Hashtags(self):
        # Test cleaning a tweet with various elements
        tweet_text = "I need to clean my room #awesome"
        print("Cleaned Text (Hashtags):", clean_tweet_text(tweet_text))
        expected_cleaned_text = "I need to clean my room  awesome"
        print("Expected Cleaned Text:", expected_cleaned_text)
        self.assertEqual(clean_tweet_text(tweet_text), expected_cleaned_text)


    def test_clean_tweet_text_Clean(self):

        # Test cleaning a tweet without any elements to clean
        tweet_text = "This is a clean tweet."
        expected_cleaned_text = "This is a clean tweet."
        print("Cleaned Text:", clean_tweet_text(tweet_text))
        print("Expected Cleaned Text:", expected_cleaned_text)
        self.assertEqual(clean_tweet_text(tweet_text), expected_cleaned_text)

if __name__ == '__main__':
    unittest.main()
