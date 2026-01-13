import asyncio
import concurrent.futures
import os
from typing import Any, Callable, Optional

# Import yt_dlp if needed


def run_async_tasks(
    tasks: list[Callable[[], Any]], max_workers: Optional[int] = None
) -> list[Any]:
    """
    Run a list of async tasks concurrently and return their results.

    Args:
        tasks: A list of callable async tasks.
        max_workers: Maximum number of workers for the thread pool. If None, it uses the default.

    Returns:
        A list of results from the tasks.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task) for task in tasks]
        return [future.result() for future in concurrent.futures.as_completed(futures)]


async def run_asyncio_tasks(tasks: list[Any]) -> list[Any]:
    """
    Run a list of asyncio tasks concurrently and return their results.

    Args:
        tasks: A list of coroutines.

    Returns:
        A list of results from the tasks.
    """
    return await asyncio.gather(*tasks)


async def run_concurrently(tasks: list[Any]) -> list[Any]:
    """
    Run a list of async tasks concurrently and return their results.

    Args:
        tasks: A list of coroutines.

    Returns:
        A list of results from the tasks.
    """
    return await run_asyncio_tasks(tasks)


async def async_download_video(
    video_url: str, output_path: str = "downloads"
) -> Optional[str]:
    """
    Downloads a YouTube video asynchronously and returns the path to the downloaded file.

    Args:
        video_url: URL of the YouTube video to download.
        output_path: Directory to save the downloaded video.

    Returns:
        Path to the downloaded video file, or None if download failed.
    """
    # Import aiohttp if needed

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        import aiohttp  # type: ignore

        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                content = await response.read()
                return content
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise
