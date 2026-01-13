from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel  # type: ignore


class VideoMetadata(BaseModel):
    """Schema for video metadata."""

    video_id: str
    title: str
    description: str
    upload_date: datetime
    duration: int  # Duration in seconds
    thumbnail_url: Optional[str] = None
    channel_name: Optional[str] = None


class TranscriptSegment(BaseModel):
    """Schema for a segment of a video transcript."""

    text: str
    start_time: float  # Start time in seconds
    end_time: float  # End time in seconds
    speaker: Optional[str] = None


class Insight(BaseModel):
    """Schema for an insight extracted from a video transcript."""

    text: str
    timestamp: float  # Timestamp in seconds
    category: str
    confidence: Optional[float] = None  # Confidence score from AI model


class VideoInsights(BaseModel):
    """Schema for insights extracted from a video."""

    video_metadata: VideoMetadata
    insights: List[Insight]
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
