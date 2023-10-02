import asyncio
from datetime import timedelta
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Protocol

from limited.base_limiter import BaseLimiter, ParamsT, ReturnT


class AsyncSemaphore(Protocol):
    def __init__(self, limit: int) -> None:
        pass

    async def acquire(self) -> Any:
        pass

    def release(self) -> Any:
        pass


class AsyncLimiter(BaseLimiter):
    """Async based limiter."""

    def __init__(
        self,
        limit: int,
        every: int | float | timedelta | None = None,
        semaphore: type[AsyncSemaphore] = asyncio.Semaphore,
        sleep: Callable[[float], Any] = asyncio.sleep,
        create_task: Callable[[Coroutine], Any] = asyncio.create_task,
    ) -> None:
        super().__init__(limit, every)
        self._semaphore = semaphore(limit)
        self._sleep = sleep
        self._create_task = create_task
        # strong reference to all tasks, prevents them from being garbage collected.
        self._tasks = set()

    def _wrap_async_function(
        self, func: Callable[ParamsT, Awaitable[ReturnT]]
    ) -> Callable[ParamsT, Awaitable[ReturnT]]:
        @wraps(func)
        async def wrapper(*args: ParamsT.args, **kwargs: ParamsT.kwargs) -> ReturnT:
            await self._semaphore.acquire()
            try:
                return await func(*args, **kwargs)
            finally:
                task = self._create_task(self._release_task())
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)

        return wrapper

    async def _release_task(self) -> None:
        await self._sleep(self._every)
        self._semaphore.release()
