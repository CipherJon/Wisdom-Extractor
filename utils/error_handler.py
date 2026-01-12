class VideoNotFoundError(Exception):
    """Raised when a video is not found or cannot be accessed."""

    pass


class TranscriptNotAvailableError(Exception):
    """Raised when a transcript is not available for a video."""

    pass


class AIProcessingError(Exception):
    """Raised when there is an error during AI processing."""

    pass


class InvalidVideoURLError(Exception):
    """Raised when the provided video URL is invalid."""

    pass


class DatabaseConnectionError(Exception):
    """Raised when there is an error connecting to the database."""

    pass


class StorageError(Exception):
    """Raised when there is an error during file storage operations."""

    pass


class AuthenticationError(Exception):
    """Raised when there is an error during authentication."""

    pass


class ConfigurationError(Exception):
    """Raised when there is an error in the configuration."""

    pass


class APIKeyNotFoundError(Exception):
    """Raised when an API key is not found or is invalid."""

    pass


class ConcurrentTaskError(Exception):
    """Raised when there is an error during concurrent task execution."""

    pass


def handle_errors(func):
    """
    Decorator to handle exceptions globally.
    Logs the error and re-raises it for further handling.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the error here if logging is configured
            print(f"An error occurred: {e}")
            raise

    return wrapper
