def extract_insights(self, transcript: str, max_tokens: int = 1000) -> List[Insight]:
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

        insights = self._parse_insights(content)

        if not insights:
            raise ValueError("No valid insights could be parsed from the response")

        return insights

    except Exception as e:
        logger.error(f"Error extracting insights: {e}")
        raise RuntimeError(f"Failed to extract insights: {str(e)}") from e
