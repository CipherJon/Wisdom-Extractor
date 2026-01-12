import unittest
from unittest.mock import MagicMock, patch

from data.models import Insight
from utils.ai_processor import AIProcessor


class TestAIProcessor(unittest.TestCase):
    def setUp(self):
        self.transcript = "This is a sample transcript for testing purposes."
        with patch("openai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            self.ai_processor = AIProcessor(api_key="dummy_api_key")
            self.ai_processor.client = mock_client

    @patch("openai.OpenAI")
    def test_extract_insights(self, mock_openai):
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock the chat completions response with proper format
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.content = """
        Here are the extracted insights:
        - First important wisdom from the video
        - Second deep observation
        """
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        # Set the return_value for the content attribute
        mock_response.choices[0].message.content = """
        Here are the extracted insights:
        - First important wisdom from the video
        - Second deep observation
        """
        mock_client.chat.completions.create.return_value = mock_response

        insights = self.ai_processor.extract_insights(self.transcript)

        # Debug output
        print(f"Insights: {insights}")
        print(f"Insights length: {len(insights)}")

        # Verify the insights are correctly parsed
        self.assertIsInstance(insights, list)
        self.assertGreaterEqual(len(insights), 1)
        self.assertIsInstance(insights[0], Insight)
        self.assertIn("First important wisdom", insights[0].text)

    @patch("openai.OpenAI")
    def test_extract_insights_empty_response(self, mock_openai):
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock an empty response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = ""
        mock_client.chat.completions.create.return_value = mock_response

        insights = self.ai_processor.extract_insights(self.transcript)

        # Verify no insights are returned
        self.assertEqual(len(insights), 0)

    @patch("openai.OpenAI")
    def test_extract_insights_error_handling(self, mock_openai):
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock an API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with self.assertRaises(RuntimeError):
            self.ai_processor.extract_insights(self.transcript)


if __name__ == "__main__":
    unittest.main()
