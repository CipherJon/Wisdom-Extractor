import unittest
from unittest.mock import MagicMock, patch

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

from app import get_transcript


# Monkey patch get_transcript method for testing
class MockTranscriptSnippet:
    def __init__(self, text, start, duration):
        self.text = text
        self.start = start
        self.duration = duration


def get_transcript_mock(*args, **kwargs):
    return [
        MockTranscriptSnippet("Hello", 0.0, 1.0),
        MockTranscriptSnippet("World", 1.0, 1.0),
    ]


YouTubeTranscriptApi.get_transcript = get_transcript_mock


class TestTranscriptHandling(unittest.TestCase):
    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_successful_transcript_fetch(self, mock_get_transcript):
        # Mock transcript data
        class MockSnippet:
            def __init__(self, text, start, duration):
                self.text = text
                self.start = start
                self.duration = duration

        mock_transcript = [
            MockSnippet("Hello", 0.0, 1.0),
            MockSnippet("World", 1.0, 1.0),
        ]
        mock_get_transcript.return_value = mock_transcript

        result = get_transcript("test_video_id")
        self.assertIn("Hello", result)
        self.assertIn("World", result)
        mock_get_transcript.assert_called_once_with(
            "test_video_id",
            languages=["en", "en-US", "en-GB"],
            preserve_formatting=True,
        )

    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_transcripts_disabled(self, mock_get_transcript):
        # Create a mock exception with required arguments
        mock_exception = TranscriptsDisabled(video_id="test_video_id")
        mock_get_transcript.side_effect = mock_exception

        result = get_transcript("test_video_id")
        self.assertEqual(result, "Error: This video has transcripts disabled.")

    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_no_transcript_found(self, mock_get_transcript):
        # Create a mock exception with required arguments
        mock_exception = NoTranscriptFound(
            video_id="test_video_id",
            requested_language_codes=["en"],
            transcript_data={},
        )
        mock_get_transcript.side_effect = mock_exception

        result = get_transcript("test_video_id")
        self.assertEqual(
            result,
            "Error: No transcript found for this video. The video might not have captions available.",
        )

    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_generic_error(self, mock_get_transcript):
        mock_get_transcript.side_effect = Exception("Test error")

        result = get_transcript("test_video_id")
        self.assertEqual(
            result, "Error getting transcript after 3 attempts: Test error"
        )


if __name__ == "__main__":
    unittest.main()
