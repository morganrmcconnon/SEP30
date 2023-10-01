import unittest
from translate_text import detect_and_translate_language

class TestTranslateText(unittest.TestCase):

    def test_translate_text(self):
        # Define test cases with text to be translated
        test_cases = [
            # Test case 1
            {
                "text": "Hello, how are you?",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "en",
            },
            # Test case 2
            {
                "text": "Bonjour, comment ça va?",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "fr",
            },
            # Test case 3
            {
                "text": "Hola, ¿cómo estás?",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "es",
            },
            # Test case 4
            {
                "text": "Ciao, come stai?",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "it",
            },
            # Test case 5
            {
                "text": "你好，你好吗？",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "zh-CN",
            },
            # Test case 6
            {
                "text": "Привет, как вы?",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "ru",
            },
            # Test case 7
            {
                "text": "こんにちは、お元気ですか？",
                "expected_translation": "Hello, how are you?",
                "expected_source_language": "ja",
            },
        ]

        for test_case in test_cases:
            text_to_translate = test_case["text"]
            expected_translation = test_case["expected_translation"]
            expected_source_language = test_case["expected_source_language"]

            # Call the detect_and_translate_language function
            translated_text, source_language, _, _ = detect_and_translate_language(text_to_translate)

            # Assert that the translated text and source language match the expected values
            self.assertEqual(translated_text, expected_translation)
            self.assertEqual(source_language, expected_source_language)

if __name__ == "__main__":
    unittest.main()
