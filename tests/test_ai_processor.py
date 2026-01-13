import unittest
from unittest.mock import MagicMock, patch

from data.models import Insight
from utils.ai_processor import AIProcessor


class MockMessage:
    """Custom mock class that properly handles content attribute access"""

    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content


class MockChoice:
    """Custom mock class that properly handles message attribute access"""

    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message


class MockChoices:
    """Custom mock class that properly handles choices indexing"""

    def __init__(self, choice):
        self._choice = choice

    def __getitem__(self, index):
        return self._choice


class MockResponse:
    """Custom mock class that properly handles response structure"""

    def __init__(self, choice):
        self._choices = MockChoices(choice)

    @property
    def choices(self):
        return self._choices


class TestAIProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.transcript = "This is a sample transcript for testing purposes."
        with patch("openai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            self.ai_processor = AIProcessor(api_key="dummy_api_key")
            self.ai_processor.client = mock_client

    @patch("openai.OpenAI")
    def test_extract_insights(self, mock_openai):
        """Test successful extraction of insights from transcript."""
        # Create the innermost message with actual content
        mock_message = MockMessage(
            """
Here are the extracted insights:
- First important wisdom from the video
- Second deep observation
        """.strip()
        )

        # Create choice with message
        mock_choice = MockChoice(mock_message)

        # Create response with choices
        mock_response = MockResponse(mock_choice)

        # Create client mock
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        # Set up the OpenAI mock
        mock_openai.return_value = mock_client

        # Override the processor's client to use our mock
        self.ai_processor.client = mock_client

        # Extract insights
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
        """Test handling of empty response from AI."""
        # Create the innermost message with empty content
        mock_message = MockMessage("")

        # Create choice with message
        mock_choice = MockChoice(mock_message)

        # Create response with choices
        mock_response = MockResponse(mock_choice)

        # Create client mock
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        # Set up the OpenAI mock
        mock_openai.return_value = mock_client

        # Override the processor's client to use our mock
        self.ai_processor.client = mock_client

        # Should raise RuntimeError for empty response
        with self.assertRaises(RuntimeError):
            _ = self.ai_processor.extract_insights(self.transcript)

    @patch("openai.OpenAI")
    def test_extract_insights_error_handling(self, mock_openai):
        """Test error handling when AI API fails."""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock an API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # Should raise RuntimeError for API errors
        with self.assertRaises(RuntimeError):
            _ = self.ai_processor.extract_insights(self.transcript)


if __name__ == "__main__":
    unittest.main()
