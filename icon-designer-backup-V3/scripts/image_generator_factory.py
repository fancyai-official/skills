"""Image generator factory.

Remote generation and file publishing logic has been removed.
Only local placeholder interfaces remain so older imports do not fail immediately.
"""

from nano_banana_image_generator import step1_submit_task, step2_poll_task, step3_get_result
from nano_banana_batch_util import (
    batch_step1_submit_tasks as _batch_step1,
    batch_step2_poll_tasks as _batch_step2,
    batch_step3_get_results as _batch_step3,
)
from typing import List, Dict


# ============================================================
# Batch interface wrappers. Keep the previous function signatures.
# ============================================================

def batch_step1_submit_tasks(tasks: List[Dict], max_workers: int = 3) -> List[Dict]:
    """Call the local placeholder submit interface in batches."""
    return _batch_step1(step1_submit_task, tasks, max_workers)


def batch_step2_poll_tasks(
    task_infos: List[Dict],
    max_poll_time: int = 50,
    max_workers: int = 9
) -> List[Dict]:
    """Call the local placeholder result-check interface in batches."""
    return _batch_step2(step2_poll_task, task_infos, max_poll_time, max_workers)


def batch_step3_get_results(
    file_infos: List[Dict],
    max_workers: int = 3
) -> List[Dict]:
    """Call the local placeholder result interface in batches."""
    return _batch_step3(step3_get_result, file_infos, max_workers)


# ============================================================
# Explicit public interface list.
# ============================================================


__all__ = [
    # Single-task three-step interface.
    "step1_submit_task",
    "step2_poll_task",
    "step3_get_result",
    # Batch processing interface.
    "batch_step1_submit_tasks",
    "batch_step2_poll_tasks",
    "batch_step3_get_results",
]
