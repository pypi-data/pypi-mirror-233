import inspect
from datetime import timedelta
from typing import Awaitable, Callable, ParamSpec, TypeVar

ReturnT = TypeVar("ReturnT")
ParamsT = ParamSpec("ParamsT")


class BaseLimiter:
    def __init__(
        self, limit: int, every: int | float | timedelta | None = None
    ) -> None:
        self._limit = self._validate_limit(limit)
        self._every = self._validate_every(every)

    def __call__(self, func: Callable[ParamsT, ReturnT]) -> Callable[ParamsT, ReturnT]:
        if inspect.iscoroutinefunction(func):
            return self._wrap_async_function(func)
        else:
            return self._wrap_sync_function(func)

    def _wrap_sync_function(
        self, func: Callable[ParamsT, ReturnT]
    ) -> Callable[ParamsT, ReturnT]:
        raise NotImplementedError(
            f"Can't limit synchronic functions using {self.__class__.__name__}"
        )

    def _wrap_async_function(
        self, func: Callable[ParamsT, Awaitable[ReturnT]]
    ) -> Callable[ParamsT, Awaitable[ReturnT]]:
        raise NotImplementedError(
            f"Can't limit asynchronous functions using {self.__class__.__name__}"
        )

    @classmethod
    def _validate_limit(cls, limit: int) -> int:
        if not isinstance(limit, int) or limit < 1:
            raise ValueError(f"limit must be a positive integer (got {limit!r})")
        return limit

    @classmethod
    def _validate_every(cls, every: int | float | timedelta | None) -> float | None:
        if not every:
            return None

        if isinstance(every, timedelta):
            every = every.total_seconds()

        if not isinstance(every, (int, float)) or every < 0:
            raise ValueError(
                "evert must be a non-negative number, or a positive timedelta instance"
            )

        return every
