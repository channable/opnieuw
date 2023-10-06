from __future__ import annotations

from contextlib import AbstractContextManager

from .retries import WaitState, replace_wait_state


class WaitLessWaitState(WaitState):
    def get_seconds_to_wait(self) -> float | None:
        if self.waits + 1 >= self.max_calls_total:
            return None
        self.waits += 1
        return 0


def retry_immediately(namespace: str | None = None) -> AbstractContextManager[None]:
    """
    Returns a contextmanager that prevents waits between retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not wait.
    """
    return replace_wait_state(WaitLessWaitState, namespace=namespace)
