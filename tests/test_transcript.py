import unittest
from unittest.mock import patch

from app import get_transcript


class TestTranscriptHandling(unittest.TestCase):
    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_successful_transcript_fetch(self, mock_get_transcript):
        # Mock transcript data - YouTubeTranscriptApi returns list of dicts
        mock_transcript = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]
        mock_get_transcript.return_value = mock_transcript

        result = get_transcript("test_video_id")
        self.assertIsNotNone(result)
        self.assertIn("Hello", result)
        self.assertIn("World", result)
        mock_get_transcript.assert_called_once_with(
            "test_video_id",
            languages=["en", "en-US", "en-GB"],
            preserve_formatting=True,
        )

    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_no_transcript_found(self, mock_get_transcript):
        from youtube_transcript_api import NoTranscriptFound

        mock_get_transcript.side_effect = NoTranscriptFound(
            video_id="test_video_id",
            requested_language_codes=["en"],
            transcript_data={},
        )
        result = get_transcript("test_video_id")
        self.assertEqual(
            result,
            "Error: No transcript found for this video. The video might not have captions available.",
        )

    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_transcripts_disabled(self, mock_get_transcript):
        from youtube_transcript_api import TranscriptsDisabled

        mock_get_transcript.side_effect = TranscriptsDisabled(video_id="test_video_id")
        result = get_transcript("test_video_id")
        self.assertEqual(result, "Error: This video has transcripts disabled.")

    @patch("app.YouTubeTranscriptApi.get_transcript")
    def test_generic_error(self, mock_get_transcript):
        mock_get_transcript.side_effect = Exception("Some error")
        result = get_transcript("test_video_id", retries=1)
        self.assertIsNotNone(result)
        self.assertIn("Error getting transcript after 1 attempts", result)


if __name__ == "__main__":
    unittest.main()
