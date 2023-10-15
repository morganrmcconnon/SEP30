import unittest
from unittest.mock import patch, Mock
from ..translate_text import detect_and_translate_language, TRANSLATOR

class TestTranslateText(unittest.TestCase):

    @patch.object(TRANSLATOR, 'translate')
    def test_detect_and_translate_language(self, mock_translate):
        # Mock the translate method to return a fixed response
        mock_translation = Mock()
        mock_translation.text = "Hello, how are you?"
        mock_translation.src = "en"
        mock_translation.pronunciation = None
        mock_translation.extra_data = {}
        mock_translate.return_value = mock_translation

        # Define a test case
        text_to_translate = "Hello, how are you?"
        expected_translation = "Hello, how are you?"
        expected_source_language = "en"

        # Call the detect_and_translate_language function
        translated_text, source_language, _, _ = detect_and_translate_language(text_to_translate)

        # Assert that the translated text and source language match the expected values
        self.assertEqual(translated_text, expected_translation)
        self.assertEqual(source_language, expected_source_language)

if __name__ == "__main__":
    unittest.main()
