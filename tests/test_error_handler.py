import pytest

from utils.error_handler import InvalidVideoURLError, VideoNotFoundError, handle_errors


def test_video_not_found_error():
    """Test that VideoNotFoundError is raised correctly."""
    with pytest.raises(VideoNotFoundError):
        raise VideoNotFoundError("Video not found")


def test_invalid_url_error():
    """Test that InvalidVideoURLError is raised correctly."""
    with pytest.raises(InvalidVideoURLError):
        raise InvalidVideoURLError("Invalid URL provided")


def test_handle_errors_decorator():
    """Test that handle_errors decorator logs and re-raises exceptions."""

    @handle_errors
    def test_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        test_function()
