import logging
from typing import List, Optional

from openai import OpenAI

from data.models import Insight

logger = logging.getLogger(__name__)


class AIProcessor:
    """A processor for extracting insights from video transcripts using AI."""

    def __init__(self, api_key: str):
        """
        Initialize the AIProcessor with an OpenAI API key.

        Args:
            api_key: The OpenAI API key for authentication.
        """
        self.client = OpenAI(api_key=api_key)

    def extract_insights(
        self, transcript: str, max_tokens: int = 1000
    ) -> List[Insight]:
        """
        Extract insights from a video transcript using OpenAI's API.
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

            # Force evaluation of the content (critical for mocks!)
            content = str(response.choices[0].message.content).strip()

            logger.debug(f"Raw insights text: {content!r}")
            print(f"DEBUG: Content to parse: {content!r}")

            insights = self._parse_insights(content)

            if not insights:
                raise ValueError("No valid insights could be parsed from the response")

            return insights

        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            raise RuntimeError(f"Failed to extract insights: {str(e)}") from e

    def _parse_insights(self, content: str) -> List[Insight]:
        """
        Parse raw content from the AI response into structured Insight objects.

        Args:
            content: Raw text content from the AI response.

        Returns:
            List of Insight objects parsed from the content.
        """
        insights = []
        # Split content by lines and filter out empty lines
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        for line in lines:
            # Skip lines that don't start with a bullet point
            if not line.startswith("-"):
                continue

            # Extract the insight text
            insight_text = line[1:].strip()
            if insight_text:
                insights.append(
                    Insight(
                        text=insight_text,
                        timestamp=0.0,  # Default timestamp
                        category="general",  # Default category
                    )
                )

        return insights
