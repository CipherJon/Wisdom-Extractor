import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from utils.concurrency import async_download_video, run_concurrently


@pytest.mark.asyncio
async def test_run_concurrently_success():
    """Test that run_concurrently executes tasks concurrently and returns results."""

    async def mock_task(task_id):
        await asyncio.sleep(0.1)
        return f"Result-{task_id}"

    tasks = [mock_task(i) for i in range(3)]
    results = await run_concurrently(tasks)

    assert len(results) == 3
    assert all(isinstance(result, str) for result in results)
    assert "Result-0" in results


@pytest.mark.asyncio
async def test_run_concurrently_empty():
    """Test that run_concurrently handles an empty task list."""
    results = await run_concurrently([])
    assert results == []


@pytest.mark.asyncio
async def test_async_download_video_success():
    """Test that async_download_video downloads a video successfully."""
    mock_url = "https://example.com/video.mp4"
    mock_content = b"fake video content"

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.read.return_value = mock_content
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await async_download_video(mock_url)
        assert result == mock_content


@pytest.mark.asyncio
async def test_async_download_video_failure():
    """Test that async_download_video handles download failures."""
    mock_url = "https://example.com/video.mp4"

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.side_effect = Exception("Download failed")

        with pytest.raises(Exception, match="Download failed"):
            await async_download_video(mock_url)
