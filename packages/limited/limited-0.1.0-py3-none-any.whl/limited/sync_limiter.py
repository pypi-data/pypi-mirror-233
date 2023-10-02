import threading
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Protocol

from limited.base_limiter import BaseLimiter, ParamsT, ReturnT


class SyncSemaphore(Protocol):
    def __init__(self, limit: int) -> None:
        pass

    def acquire(self) -> Any:
        pass

    def release(self) -> Any:
        pass


class SyncLimiter(BaseLimiter):
    """Thread based limiter."""

    def __init__(
        self,
        limit: int,
        every: int | float | timedelta | None = None,
        semaphore: type[SyncSemaphore] = threading.Semaphore,
    ) -> None:
        super().__init__(limit, every)
        self._semaphore = semaphore(limit)

    def _wrap_sync_function(
        self, func: Callable[ParamsT, ReturnT]
    ) -> Callable[ParamsT, ReturnT]:
        @wraps(func)
        def wrapper(*args: ParamsT.args, **kwargs: ParamsT.kwargs) -> ReturnT:
            self._semaphore.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                self._start_release_timer()

        return wrapper

    def _start_release_timer(self):
        if self._every:
            timer = threading.Timer(
                interval=self._every,
                function=self._semaphore.release,
            )
            timer.daemon = True
            timer.start()
