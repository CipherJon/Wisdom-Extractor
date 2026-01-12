import unittest
from datetime import datetime

from data.models import Insight, Transcript, TranscriptSegment, VideoMetadata


class TestModels(unittest.TestCase):
    def test_video_metadata_initialization(self):
        metadata = VideoMetadata(
            video_id="test_id",
            title="Test Video",
            description="Test Description",
            upload_date=datetime(2023, 1, 1),
            duration=3600,
            thumbnail_url="http://example.com/thumbnail.jpg",
            channel_name="Test Channel",
        )
        self.assertEqual(metadata.video_id, "test_id")
        self.assertEqual(metadata.title, "Test Video")
        self.assertEqual(metadata.description, "Test Description")
        self.assertEqual(metadata.duration, 3600)
        self.assertEqual(metadata.upload_date, datetime(2023, 1, 1))
        self.assertEqual(metadata.thumbnail_url, "http://example.com/thumbnail.jpg")
        self.assertEqual(metadata.channel_name, "Test Channel")

    def test_transcript_initialization(self):
        segments = [
            TranscriptSegment(
                text="This is a test transcript.", start_time=0.0, end_time=1.0
            )
        ]
        transcript = Transcript(video_id="test_id", language="en", segments=segments)
        self.assertEqual(transcript.video_id, "test_id")
        self.assertEqual(transcript.language, "en")
        self.assertEqual(len(transcript.segments), 1)
        self.assertEqual(transcript.segments[0].text, "This is a test transcript.")

    def test_insight_initialization(self):
        insight = Insight(
            text="This is a test insight.",
            timestamp=120.0,
            category="Test Category",
            confidence=0.95,
        )
        self.assertEqual(insight.text, "This is a test insight.")
        self.assertEqual(insight.timestamp, 120.0)
        self.assertEqual(insight.category, "Test Category")
        self.assertEqual(insight.confidence, 0.95)


if __name__ == "__main__":
    unittest.main()
