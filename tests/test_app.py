from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from app import main


@pytest.fixture
def mock_streamlit():
    """Fixture to mock Streamlit functions."""
    with patch.multiple(
        "streamlit",
        title=MagicMock(),
        write=MagicMock(),
        error=MagicMock(),
        success=MagicMock(),
        info=MagicMock(),
        spinner=MagicMock(),  # Mock the spinner context manager
        session_state=MagicMock(),
        text_input=MagicMock(
            return_value="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ),
        button=MagicMock(return_value=True),
        text_area=MagicMock(),
        markdown=MagicMock(),
    ) as mocks:
        # Set up the spinner mock to work as a context manager
        mocks.spinner.return_value.__enter__ = MagicMock(return_value=None)
        mocks.spinner.return_value.__exit__ = MagicMock(return_value=None)
        yield mocks


def test_main(mock_streamlit):
    """Test the main function with valid URL."""
    # Mock the AI processor and YouTubeTranscriptApi
    with (
        patch("app.process_with_ai") as mock_process_with_ai,
        patch("app.YouTubeTranscriptApi") as mock_transcript_api,
        patch("app.TextFormatter") as mock_formatter,
    ):
        # Mock the get_transcript static method
        mock_get_transcript = MagicMock()
        mock_get_transcript.return_value = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]
        mock_transcript_api.get_transcript = mock_get_transcript

        # Mock the formatter
        mock_format_instance = MagicMock()
        mock_format_instance.format_transcript.return_value = "Hello World"
        mock_formatter.return_value = mock_format_instance

        # Mock AI response
        mock_process_with_ai.return_value = """
# SUMMARY
This is a test summary

# IDEAS
- Idea 1 about wisdom
- Idea 2 about insights

# INSIGHTS
- Insight 1 about life
- Insight 2 about technology
"""

        # Run the main function
        main()

        # Assertions
        mock_streamlit["title"].assert_called_once_with("Wisdom Extractor")
        mock_streamlit["text_input"].assert_called_once_with("Enter YouTube URL:")
        mock_streamlit["button"].assert_called_once_with("Extract Wisdom")
        mock_process_with_ai.assert_called_once()
        mock_streamlit["write"].assert_called()


def test_main_invalid_url(mock_streamlit):
    """Test the main function with invalid URL."""
    # Mock the AI processor and YouTubeTranscriptApi to raise an exception
    with (
        patch("app.process_with_ai") as mock_process_with_ai,
        patch("app.YouTubeTranscriptApi") as mock_transcript_api,
    ):
        # Mock the get_transcript static method to raise exception
        mock_get_transcript = MagicMock()
        mock_get_transcript.side_effect = Exception("Transcript not available")
        mock_transcript_api.get_transcript = mock_get_transcript
        mock_process_with_ai.side_effect = Exception("Invalid URL")

        # Run the main function
        main()

        # Assertions
        mock_streamlit["title"].assert_called_once_with("Wisdom Extractor")
        mock_streamlit["text_input"].assert_called_once_with("Enter YouTube URL:")
        mock_streamlit["button"].assert_called_once_with("Extract Wisdom")
        mock_process_with_ai.assert_called_once()
        mock_streamlit["error"].assert_called_once_with("Error: Invalid URL")
