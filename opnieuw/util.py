from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager

from .retries import DoWait, RetryState, replace_retry_state


class NoRetryState(RetryState):
    def __iter__(self) -> Iterator[DoWait]:
        # Yield a DoWait that leads to no waiting
        yield DoWait(0, 0, 0, 0)


def no_retries(namespace: str | None = None) -> AbstractContextManager[None]:
    """
    Returns a contextmanager that disables retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not retry.
    """
    return replace_retry_state(NoRetryState, namespace=namespace)
