import os
from typing import List, Optional
from contextlib import contextmanager

from openai import OpenAI

from data.models import Insight
from logging_utils.logger import get_logger

logger = get_logger(__name__)

class AIProcessor:
    """
    Core AI logic for extracting insights from video transcripts using OpenAI's API.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AIProcessor with an OpenAI API key.

        Args:
            api_key (Optional[str]): OpenAI API key. If not provided, it will be loaded from environment variables.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided and not found in environment variables."
            )
        self.client = OpenAI(api_key=self.api_key)

    def extract_insights(
        self, transcript: str, max_tokens: int = 1000
    ) -> List[Insight]:
        """
        Extract insights from a video transcript using OpenAI's API.

        Args:
            transcript (str): The transcript text from the video.
            max_tokens (int): Maximum number of tokens to use for the API call.

        Returns:
            List[Insight]: A list of extracted insights.

        Raises:
            RuntimeError: If there's an error extracting insights from the API.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts key insights from video transcripts.",
                    },
                    {
                        "role": "user",
                        "content": f"Extract key insights from the following transcript:\n\n{transcript}",
                    },
                ],
                max_tokens=max_tokens,
            )

            insights_text = response.choices[0].message.content
            insights = self._parse_insights(insights_text)
            return insights
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            raise RuntimeError(f"Failed to extract insights: {str(e)}") from e

    def _parse_insights(self, insights_text: str) -> List[Insight]:
        """
        Parse the raw insights text into a list of Insight objects.

        Args:
            insights_text (str): Raw text containing insights.

        Returns:
            List[Insight]: Parsed list of insights.
        """
        insights = []
        if not insights_text or not insights_text.strip():
            return insights

        # Improved parsing logic to handle various formats
        for line in insights_text.split('\n'):
            line = line.strip()
            if line and not line.startswith(('Here are', 'extracted insights', '#', '##', '###')):
                # Remove numbering if present (e.g., "1. ", "2. ", etc.)
                if line[0].isdigit() and '.' in line[:5]:
                    line = line.split('.', 1)[1].strip()
                # Remove bullet points if present
                if line.startswith(('-', '*', '•')):
                    line = line[1:].strip()
                # Create insight if there's meaningful content
                if len(line) > 5:  # Minimum length requirement
                    insights.append(
                        Insight(text=line, timestamp=0, category="general")
                    )
        return insights
