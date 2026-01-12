import os
from typing import Optional

from dotenv import load_dotenv


class SecretsManager:
    """
    Manages sensitive information such as API keys and environment variables.
    Uses dotenv to load environment variables from a .env file.
    """

    def __init__(self, env_file: str = ".env"):
        """
        Initialize the SecretsManager with the specified .env file.

        Args:
            env_file (str): Path to the .env file. Defaults to ".env".
        """
        self.env_file = env_file
        load_dotenv(self.env_file)

    def get_secret(self, key: str) -> Optional[str]:
        """
        Retrieve a secret value from the environment variables.

        Args:
            key (str): The key of the environment variable to retrieve.

        Returns:
            Optional[str]: The value of the environment variable, or None if it does not exist.
        """
        return os.getenv(key)

    def set_secret(self, key: str, value: str) -> None:
        """
        Set a secret value in the environment variables.

        Args:
            key (str): The key of the environment variable to set.
            value (str): The value to set for the environment variable.
        """
        os.environ[key] = value

    def load_secrets(self) -> dict:
        """
        Load all secrets from the .env file into a dictionary.

        Returns:
            dict: A dictionary containing all the environment variables.
        """
        return dict(os.environ)
