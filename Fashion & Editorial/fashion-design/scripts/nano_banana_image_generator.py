"""Local placeholder interface for the Nano Banana image generator.

Remote image generation, polling, download, and file publishing logic has been removed.
This module keeps the old function names only to make it explicit that this repository
no longer includes networked generation or file publishing implementations.
"""

from typing import List, Optional


def _disabled() -> None:
    print("[ERROR] Remote image generation and file publishing logic has been removed. Use the host environment's image generation capability instead.")


def step1_submit_task(
    img_urls: Optional[List[str]] = None,
    prompt: str = "",
    ratio: str = "1:1",
    resolution: str = "2K",
) -> Optional[str]:
    """Legacy placeholder: remote task submission is no longer available."""
    _disabled()
    return None


def step2_poll_task(
    task_id: str,
    max_poll_time: int = 50,
) -> Optional[str]:
    """Legacy placeholder: remote task polling is no longer available."""
    _disabled()
    return None


def step3_get_result(
    file_url: str
) -> Optional[str]:
    """Legacy placeholder: remote result download and file publishing are no longer available."""
    _disabled()
    return None
