from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="verivid-job")
_active_videos: set[str] = set()
_active_lock = Lock()


class JobExecutor(ABC):

  @abstractmethod
  def submit(self, video_id: str, fn: Callable[[], None]) -> bool:
    """
    Schedule work for a video.

    Returns True when the job was accepted; False when already active.
    """


class InProcessJobExecutor(JobExecutor):
  """
  In-process background execution.

  Limitations:
  - Jobs do not survive server restarts.
  - No distributed queue or horizontal scaling.
  - Duplicate submissions for the same video are rejected while active.
  """

  def submit(self, video_id: str, fn: Callable[[], None]) -> bool:
    with _active_lock:
      if video_id in _active_videos:
        return False
      _active_videos.add(video_id)

    def _runner() -> None:
      try:
        fn()
      finally:
        with _active_lock:
          _active_videos.discard(video_id)

    _executor.submit(_runner)
    return True

  @staticmethod
  def is_active(video_id: str) -> bool:
    with _active_lock:
      return video_id in _active_videos


job_executor: JobExecutor = InProcessJobExecutor()