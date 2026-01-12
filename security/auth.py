# auth.py
# Handles user authentication if needed (e.g., Streamlit secrets or OAuth for YouTube API)

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AuthManager:
    """
    Manages authentication for the application.
    Supports loading API keys and secrets from environment variables.
    """

    @staticmethod
    def get_api_key(key_name: str) -> Optional[str]:
        """
        Retrieves an API key from environment variables.

        Args:
            key_name (str): The name of the environment variable storing the API key.

        Returns:
            Optional[str]: The API key if found, otherwise None.
        """
        return os.getenv(key_name)

    @staticmethod
    def validate_api_key(key_name: str) -> bool:
        """
        Validates if an API key exists in the environment variables.

        Args:
            key_name (str): The name of the environment variable storing the API key.

        Returns:
            bool: True if the API key exists, otherwise False.
        """
        return key_name in os.environ and os.environ[key_name] is not None
