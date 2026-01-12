```python
import os
from typing import Any, Dict, Optional

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def download_video(video_url: str, output_path: str = "downloads") -> Optional[str]:
    """
    Downloads a YouTube video and returns the path to the downloaded file.

    Args:
        video_url: URL of the YouTube video to download.
        output_path: Directory to save the downloaded video.

    Returns:
        Path to the downloaded video file, or None if download failed.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            return video_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def get_video_transcript(video_id: str) -> Optional[str]:
    """
    Fetches the transcript of a YouTube video using its video ID.

    Args:
        video_id: YouTube video ID.

    Returns:
        Transcript text as a string, or None if fetching failed.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def save_transcript_to_file(transcript_text: str, file_path: str) -> bool:
    """
    Saves the transcript text to a file.

    Args:
        transcript_text: Transcript text to save.
        file_path: Path to the file where the transcript will be saved.

    Returns:
        True if the transcript was saved successfully, False otherwise.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(transcript_text)
        return True
    except Exception as e:
        print(f"Error saving transcript to file: {e}")
        return False

def read_file(file_path: str) -> Optional[str]:
    """
    Reads the content of a file.

    Args:
        file_path: Path to the file to read.

    Returns:
        Content of the file as a string, or None if reading failed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def download_youtube_video(
    video_url: str, output_path: str = "downloads"
) -> Optional[str]:
    """
    Downloads a YouTube video and returns the path to the downloaded file.

    Args:
        video_url: URL of the YouTube video to download.
        output_path: Directory to save the downloaded video.

    Returns:
        Path to the downloaded video file, or None if download failed.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            return video_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise

def download_transcript(
    video_id: str, output_path: str = "transcripts"
) -> Optional[str]:
    """
    Downloads the transcript of a YouTube video and saves it to a file.

    Args:
        video_id: YouTube video ID.
        output_path: Directory to save the transcript file.

    Returns:
        Path to the saved transcript file, or None if the operation failed.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    transcript_text = get_video_transcript(video_id)
    if not transcript_text:
        return None

    file_path = os.path.join(output_path, f"{video_id}.txt")
    if save_transcript_to_file(transcript_text, file_path):
        return file_path
    else:
        return None

def save_to_file(file_path: str, content: str) -> bool:
    """
    Saves content to a file.

    Args:
        file_path: Path to the file where the content will be saved.
        content: Content to save.

    Returns:
        True if the content was saved successfully, False otherwise.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def read_from_file(file_path: str) -> Optional[str]:
    """
    Reads the content of a file.

    Args:
        file_path: Path to the file to read.

    Returns:
        Content of the file as a string, or None if reading failed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading from file: {e}")
        return None
