import unittest
from ..sentiment_analysis import classify_sentiment

class TestSentimentAnalysis(unittest.TestCase):

    def test_classify_sentiment(self):
        # Define a test case with a known positive text
        text = "I love this!"

        # Call the classify_sentiment function
        sentiment, confidence_probabilities = classify_sentiment(text)

        # Print the detected sentiment and confidence probabilities for debugging purposes
        print(f"Detected sentiment: {sentiment}")
        print(f"Confidence probabilities: {confidence_probabilities}")

        # Assert that the detected sentiment is not None
        self.assertIsNotNone(sentiment)

        # Assert that the confidence probabilities are not None
        self.assertIsNotNone(confidence_probabilities)

        # Assert that the confidence probabilities contain all three sentiment categories
        self.assertIn('negative', confidence_probabilities)
        self.assertIn('neutral', confidence_probabilities)
        self.assertIn('positive', confidence_probabilities)

    def test_classify_sentiment_with_empty_text(self):
        # Define a test case with an empty text
        text = ""

        # Call the classify_sentiment function
        sentiment, confidence_probabilities = classify_sentiment(text)

        # Print the detected sentiment and confidence probabilities for debugging purposes
        print(f"Detected sentiment: {sentiment}")
        print(f"Confidence probabilities: {confidence_probabilities}")

        # Assert that the detected sentiment is not None
        self.assertIsNotNone(sentiment)

        # Assert that the confidence probabilities are not None
        self.assertIsNotNone(confidence_probabilities)

        # Assert that the confidence probabilities contain all three sentiment categories
        self.assertIn('negative', confidence_probabilities)
        self.assertIn('neutral', confidence_probabilities)
        self.assertIn('positive', confidence_probabilities)

if __name__ == "__main__":
    unittest.main()
