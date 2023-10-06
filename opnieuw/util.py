from __future__ import annotations

from contextlib import AbstractContextManager

from .retries import WaitState, replace_wait_state


class NoRetryState(WaitState):
    def get_seconds_to_wait(self) -> float | None:
        return None


def no_retries(namespace: str | None = None) -> AbstractContextManager[None]:
    """
    Returns a contextmanager that disables retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not retry.
    """
    return replace_wait_state(NoRetryState, namespace=namespace)
