import unittest
from unittest.mock import patch, MagicMock
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound
from app import get_transcript

class TestTranscriptHandling(unittest.TestCase):
    @patch('app.YouTubeTranscriptApi.get_transcript')
    def test_successful_transcript_fetch(self, mock_get_transcript):
        # Mock transcript data
        mock_transcript = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0}
        ]
        mock_get_transcript.return_value = mock_transcript
        
        result = get_transcript('test_video_id')
        self.assertIn('Hello', result)
        self.assertIn('World', result)
        mock_get_transcript.assert_called_once_with('test_video_id')

    @patch('app.YouTubeTranscriptApi.get_transcript')
    def test_transcripts_disabled(self, mock_get_transcript):
        # Create a mock exception with required arguments
        mock_exception = TranscriptsDisabled(video_id='test_video_id')
        mock_get_transcript.side_effect = mock_exception
        
        result = get_transcript('test_video_id')
        self.assertEqual(result, "Error: This video has transcripts disabled.")

    @patch('app.YouTubeTranscriptApi.get_transcript')
    def test_no_transcript_found(self, mock_get_transcript):
        # Create a mock exception with required arguments
        mock_exception = NoTranscriptFound(
            video_id='test_video_id',
            requested_language_codes=['en'],
            transcript_data={}
        )
        mock_get_transcript.side_effect = mock_exception
        
        result = get_transcript('test_video_id')
        self.assertEqual(result, "Error: No transcript found for this video. The video might not have captions available.")

    @patch('app.YouTubeTranscriptApi.get_transcript')
    def test_generic_error(self, mock_get_transcript):
        mock_get_transcript.side_effect = Exception("Test error")
        
        result = get_transcript('test_video_id')
        self.assertEqual(result, "Error getting transcript: Test error")

if __name__ == '__main__':
    unittest.main() 