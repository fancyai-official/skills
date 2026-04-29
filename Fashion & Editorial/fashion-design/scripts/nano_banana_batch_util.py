"""
Batch processing utility module.

Provides concurrent local placeholder helpers for batch submission, polling,
and result retrieval.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable


def batch_step1_submit_tasks(
    submit_func: Callable,
    tasks: List[Dict],
    max_workers: int = 3
) -> List[Dict]:
    """
    Submit multiple image-generation tasks in parallel.

    Each task is submitted independently through an internal thread pool.
    Returned results keep the same order as the input tasks.

    Args:
        submit_func: Single-task submit function, usually step1_submit_task.
        tasks: Task list. Each item may contain:
            task_name  (str, optional): Task label. Defaults to "task_{i}".
            img_urls   (list, optional): Reference image paths. Use None or omit for text-only prompts.
            prompt     (str): Image prompt.
            ratio      (str, optional): Aspect ratio. Defaults to "1:1".
            resolution (str, optional): Resolution, such as 1K, 2K, or 4K. Defaults to "2K".
        max_workers (int): Maximum worker thread count. Defaults to 3.

    Returns:
        A result list with the same length and order as tasks. Each item contains:
            task_name (str): Task name.
            task_id   (str|None): Submitted task ID, or None on failure.
            status    (str): "ok" or "failed".

    Output markers for outer parsers:
        [BATCH_SUBMIT]      N tasks, M workers
        [PROGRESS]          i/N - task_name: OK/FAILED
        [BATCH_SUBMIT_DONE] ok=M/N in Xs
    """
    total = len(tasks)
    results: List[Dict] = [None] * total
    completed_count = [0]

    def _submit_one(idx: int, task: Dict):
        task_name = task.get("task_name") or f"task_{idx}"
        try:
            task_id = submit_func(
                img_urls=task.get("img_urls"),
                prompt=task.get("prompt", ""),
                ratio=task.get("ratio", "1:1"),
                resolution=task.get("resolution", "2K"),
            )
            completed_count[0] += 1
            status = "ok" if task_id else "failed"
            print(f"[PROGRESS] {completed_count[0]}/{total} — {task_name}: {status.upper()}")
            return idx, {"task_name": task_name, "task_id": task_id, "status": status}
        except Exception as e:
            completed_count[0] += 1
            print(f"[PROGRESS] {completed_count[0]}/{total} — {task_name}: FAILED ({e})")
            return idx, {"task_name": task_name, "task_id": None, "status": "failed"}

    print(f"[BATCH_SUBMIT] {total} tasks, {max_workers} workers")
    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_submit_one, i, task): i for i, task in enumerate(tasks)}
        for future in as_completed(futures):
            idx, result = future.result()
            results[idx] = result

    elapsed = time.time() - start
    ok_count = sum(1 for r in results if r and r["status"] == "ok")
    print(f"[BATCH_SUBMIT_DONE] ok={ok_count}/{total} in {elapsed:.1f}s")
    return results


def batch_step2_poll_tasks(
    poll_func: Callable,
    task_infos: List[Dict],
    max_poll_time: int = 50,
    max_workers: int = 9
) -> List[Dict]:
    """
    Poll multiple task states in parallel.

    All valid tasks start polling at the same time and share the max_poll_time window.
    Entries with task_id set to None are skipped and marked as "skipped".

    Args:
        poll_func: Single-task polling function, usually step2_poll_task.
        task_infos: Task info list. Each item contains:
            task_name (str): Task name.
            task_id   (str|None): Task ID. None values are skipped.
        max_poll_time: Maximum polling time in seconds for each task. Defaults to 50.
                       If a task does not finish in time, it returns "PENDING".
        max_workers: Maximum worker thread count. Defaults to 9.

    Returns:
        A result list with the same length and order as task_infos. Each item contains:
            task_name (str): Task name.
            task_id   (str|None): Original task ID.
            file_url  (str|None): Image path, "PENDING", or None.
            status    (str): "ready", "pending", "failed", or "skipped".

    Output markers:
        [BATCH_POLL]      valid/total tasks, M workers
        [READY]           task_name
        [PENDING]         task_name
        [FAILED]          task_name
        [BATCH_POLL_DONE] ready=R pending=P failed=F skipped=S in Xs
    """
    total = len(task_infos)
    results: List[Dict] = [None] * total

    def _poll_one(idx: int, info: Dict):
        task_name = info.get("task_name") or f"task_{idx}"
        task_id = info.get("task_id")
        if not task_id:
            return idx, {"task_name": task_name, "task_id": None,
                         "file_url": None, "status": "skipped"}
        try:
            file_url = poll_func(task_id, max_poll_time=max_poll_time)
            if file_url and file_url != "PENDING":
                print(f"[READY] {task_name}")
                return idx, {"task_name": task_name, "task_id": task_id,
                             "file_url": file_url, "status": "ready"}
            elif file_url == "PENDING":
                print(f"[PENDING] {task_name}")
                return idx, {"task_name": task_name, "task_id": task_id,
                             "file_url": "PENDING", "status": "pending"}
            else:
                print(f"[FAILED] {task_name}")
                return idx, {"task_name": task_name, "task_id": task_id,
                             "file_url": None, "status": "failed"}
        except Exception as e:
            print(f"[FAILED] {task_name}: {e}")
            return idx, {"task_name": task_name, "task_id": task_id,
                         "file_url": None, "status": "failed"}

    valid_count = sum(1 for info in task_infos if info.get("task_id"))
    print(f"[BATCH_POLL] {valid_count}/{total} tasks, {max_workers} workers, max {max_poll_time}s each")
    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_poll_one, i, info): i for i, info in enumerate(task_infos)}
        for future in as_completed(futures):
            idx, result = future.result()
            results[idx] = result

    elapsed = time.time() - start
    ready   = sum(1 for r in results if r and r["status"] == "ready")
    pending = sum(1 for r in results if r and r["status"] == "pending")
    failed  = sum(1 for r in results if r and r["status"] == "failed")
    skipped = sum(1 for r in results if r and r["status"] == "skipped")
    print(f"[BATCH_POLL_DONE] ready={ready} pending={pending} failed={failed} skipped={skipped} in {elapsed:.1f}s")
    return results


def batch_step3_get_results(
    result_func: Callable,
    file_infos: List[Dict],
    max_workers: int = 3
) -> List[Dict]:
    """
    Retrieve multiple results in parallel.

    Entries with file_url set to None or "PENDING" are skipped.

    Args:
        result_func: Single-task result function, usually step3_get_result.
        file_infos: File info list. Each item contains:
            task_name (str): Task name.
            file_url  (str|None): Image path. None and "PENDING" values are skipped.
        max_workers: Maximum worker thread count. Defaults to 3.

    Returns:
        A result list with the same length and order as file_infos. Each item contains:
            task_name (str): Task name.
            file_url  (str|None): Original image path.
            image_url (str|None): Result path, or None on failure or skip.
            status    (str): "ok", "failed", or "skipped".

    Output markers:
        [BATCH_RESULT]        valid/total images, M workers
        [PROGRESS]            i/valid - task_name: OK/FAILED
        [BATCH_RESULT_DONE]   ok=M/valid in Xs
    """
    total = len(file_infos)
    results: List[Dict] = [None] * total
    valid_pairs = [
        (i, info) for i, info in enumerate(file_infos)
        if info.get("file_url") and info.get("file_url") != "PENDING"
    ]
    valid_count = len(valid_pairs)
    completed_count = [0]

    # Pre-fill skipped entries so the result list never contains None.
    for i, info in enumerate(file_infos):
        if not info.get("file_url") or info.get("file_url") == "PENDING":
            results[i] = {
                "task_name": info.get("task_name") or f"task_{i}",
                "file_url": info.get("file_url"),
                "image_url": None,
                "status": "skipped",
            }

    def _download_one(idx: int, info: Dict):
        task_name = info.get("task_name") or f"task_{idx}"
        file_url = info.get("file_url")
        try:
            image_url = result_func(file_url)
            completed_count[0] += 1
            status = "ok" if image_url else "failed"
            print(f"[PROGRESS] {completed_count[0]}/{valid_count} — {task_name}: {status.upper()}")
            return idx, {"task_name": task_name, "file_url": file_url,
                         "image_url": image_url, "status": status}
        except Exception as e:
            completed_count[0] += 1
            print(f"[PROGRESS] {completed_count[0]}/{valid_count} — {task_name}: FAILED ({e})")
            return idx, {"task_name": task_name, "file_url": file_url,
                         "image_url": None, "status": "failed"}

    print(f"[BATCH_RESULT] {valid_count}/{total} images, {max_workers} workers")
    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_download_one, i, info): i for i, info in valid_pairs}
        for future in as_completed(futures):
            idx, result = future.result()
            results[idx] = result

    elapsed = time.time() - start
    ok_count = sum(1 for r in results if r and r["status"] == "ok")
    print(f"[BATCH_RESULT_DONE] ok={ok_count}/{valid_count} in {elapsed:.1f}s")
    return results
