import unittest
from unittest.mock import patch, Mock
from ..detect_demographics import detect_demographics, M3TWITTER

class TestDetectDemographics(unittest.TestCase):

    @patch.object(M3TWITTER, 'infer')
    def test_detect_demographics(self, mock_infer):
        # Mock the infer method to return a fixed response
        mock_infer.return_value = {"123": {"age": {"18-29": 0.5, "30-39": 0.5}, "gender": {"male": 0.5, "female": 0.5}}}

        # Define a test case
        users = [{"id": "123", "name": "Test", "screen_name": "test", "description": "test", "lang": "en"}]
        expected_result = {"123": {"age": {"18-29": 0.5, "30-39": 0.5}, "gender": {"male": 0.5, "female": 0.5}}}

        # Call the detect_demographics function
        result = detect_demographics(users)

        # Assert that the result matches the expected value
        self.assertEqual(result, expected_result)

    
if __name__ == "__main__":
    unittest.main()
