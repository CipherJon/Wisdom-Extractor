import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from utils.io_utils import (
    download_transcript,
    download_youtube_video,
    read_from_file,
    save_to_file,
)

class TestIOUtils(unittest.TestCase):
    @patch("utils.io_utils.yt_dlp.YoutubeDL")
    def test_download_youtube_video_success(self, mock_yt_dlp):
        # Setup mock
        mock_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_instance
        mock_instance.extract_info.return_value = {
            "title": "Test Video",
            "id": "test_id",
            "requested_formats": [{"url": "http://example.com/video.mp4"}],
        }
        mock_instance.prepare_filename.return_value = "/tmp/Test Video.mp4"

        # Call function
        result = download_youtube_video("http://youtube.com/watch?v=test_id", "/tmp")

        # Assertions
        self.assertEqual(result, "/tmp/Test Video.mp4")
        mock_yt_dlp.assert_called_once()
        mock_instance.extract_info.assert_called_once()

    @patch("utils.io_utils.yt_dlp.YoutubeDL")
    def test_download_youtube_video_failure(self, mock_yt_dlp):
        # Setup mock to raise exception
        mock_yt_dlp.side_effect = Exception("Download failed")

        # Call function and assert exception
        with self.assertRaises(Exception) as context:
            download_youtube_video("http://youtube.com/watch?v=test_id", "/tmp")
        self.assertIn("Download failed", str(context.exception))

    @patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript")
    def test_download_transcript_success(self, mock_get_transcript):
        # Setup mock
        mock_get_transcript.return_value = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]

        # Call function
        result = download_transcript("test_id")

        # Assertions
        self.assertEqual(result, "Hello World")
        mock_get_transcript.assert_called_once_with("test_id")

    @patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript")
    def test_download_transcript_failure(self, mock_get_transcript):
        # Setup mock to raise exception
        mock_get_transcript.side_effect = Exception("Transcript not available")

        # Call function and assert exception
        with self.assertRaises(Exception) as context:
            download_transcript("test_id")
        self.assertIn("Transcript not available", str(context.exception))

    def test_save_to_file(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name

        # Call function
        save_to_file(tmp_file_path, "Test content")

        # Assertions
        with open(tmp_file_path, "r") as file:
            content = file.read()
        self.assertEqual(content, "Test content")

        # Clean up
        os.unlink(tmp_file_path)

    def test_read_from_file(self):
        # Create a temporary file with content
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"Test content")
            tmp_file_path = tmp_file.name

        # Call function
        result = read_from_file(tmp_file_path)

        # Assertions
        self.assertEqual(result, "Test content")

        # Clean up
        os.unlink(tmp_file_path)

if __name__ == "__main__":
    unittest.main()
