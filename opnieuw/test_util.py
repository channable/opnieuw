from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager

from .retries import DoWait, RetryState, replace_retry_state


class WaitLessRetryState(RetryState):
    def __iter__(self) -> Iterator[DoWait]:
        for _ in range(self.max_calls_total):
            # Yield a DoWait that leads to no waiting
            yield DoWait(0, 0, 0, 0)


def retry_immediately(namespace: str | None = None) -> AbstractContextManager[None]:
    """
    Returns a contextmanager that prevents waits between retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not wait.
    """
    return replace_retry_state(WaitLessRetryState, namespace=namespace)
