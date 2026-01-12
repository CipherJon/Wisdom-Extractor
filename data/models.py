from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class VideoMetadata:
    """Represents metadata for a YouTube video."""

    video_id: str
    title: str
    description: str
    upload_date: datetime
    duration: int  # Duration in seconds
    thumbnail_url: str
    channel_name: str


@dataclass
class Transcript:
    """Represents the transcript of a YouTube video."""

    video_id: str
    language: str
    segments: List["TranscriptSegment"]


@dataclass
class TranscriptSegment:
    """Represents a segment of a transcript with text and timing information."""

    text: str
    start_time: float  # Start time in seconds
    end_time: float  # End time in seconds


@dataclass
class Insight:
    """Represents an insight extracted from a video transcript."""

    text: str
    timestamp: float  # Timestamp in seconds
    category: str
    confidence: Optional[float] = None  # Confidence score from AI model


@dataclass
class ProcessedVideo:
    """Represents a fully processed video with metadata, transcript, and insights."""

    metadata: VideoMetadata
    transcript: Transcript
    insights: List[Insight]
