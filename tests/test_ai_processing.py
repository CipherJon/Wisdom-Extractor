import unittest
from unittest.mock import patch, MagicMock
from app import process_with_ai

class TestAIProcessing(unittest.TestCase):
    def setUp(self):
        self.sample_transcript = "This is a sample transcript for testing."
        self.error_message = "Error: Test error message"

    @patch('app.requests.post')
    def test_successful_ai_processing(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Processed wisdom content"}}]
        }
        mock_post.return_value = mock_response

        result = process_with_ai(self.sample_transcript)
        self.assertEqual(result, "Processed wisdom content")
        mock_post.assert_called_once()

    @patch('app.requests.post')
    def test_api_error(self, mock_post):
        # Mock API error
        mock_post.side_effect = Exception("API Error")
        
        result = process_with_ai(self.sample_transcript)
        self.assertEqual(result, "Error processing with AI: API Error")

    def test_error_input(self):
        # Test with error message input
        result = process_with_ai(self.error_message)
        self.assertEqual(result, self.error_message)

if __name__ == '__main__':
    unittest.main() 