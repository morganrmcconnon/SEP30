import unittest
from sentiment_analysis import classify_sentiment

class TestSentimentAnalysis(unittest.TestCase):

    def test_classify_sentiment(self):
        # Define test cases with text in the same format as the dataset
        test_cases = [
            {
                "text_original": "Feeling really down today, nothing seems to be going right. #BadDay",
                "expected_sentiment": "negative",
            },
            {
                "text_original": "Just won a lottery! Can't believe my luck. #LuckyDay",
                "expected_sentiment": "positive",
            },
            {
                "text_original": "Attending a boring lecture again. #NotInterested",
                "expected_sentiment": "negative",
            },
            {
                "text_original": "Enjoying a peaceful evening by the beach. #Relaxation",
                "expected_sentiment": "positive",
            },
            {
                "text_original": "No opinion on the matter. #Neutral",
                "expected_sentiment": "neutral",
            },
            {
                "text_original": "I'm feeling indifferent today.",
                "expected_sentiment": "neutral",
            },
            {
                "text_original": "Great news! My favorite team won the championship.",
                "expected_sentiment": "positive",
            },
            {
                "text_original": "This weather is ruining my plans. #RainyDay",
                "expected_sentiment": "negative",
            },
            {
                "text_original": "Just received a promotion at work. #Excited",
                "expected_sentiment": "positive",
            },
            {
                "text_original": "I don't care about that topic at all.",
                "expected_sentiment": "neutral",
            },
        ]

        for test_case in test_cases:
            text = test_case["text_original"]
            expected_sentiment = test_case["expected_sentiment"]

            # Call the classify_sentiment function
            sentiment, confidence_probabilities = classify_sentiment(text)

            # Assert that the sentiment matches the expected sentiment
            self.assertEqual(sentiment, expected_sentiment)

            # Assert that the confidence probabilities are valid
            self.assertGreaterEqual(confidence_probabilities[expected_sentiment], 0.0)
            self.assertLessEqual(confidence_probabilities[expected_sentiment], 1.0)

if __name__ == '__main__':
    unittest.main()

