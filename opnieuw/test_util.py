from __future__ import annotations

from contextlib import AbstractContextManager

from .retries import BackoffCalculator, replace_backoff_calculator


class WaitLessBackoff(BackoffCalculator):
    def get_backoff(self) -> float | None:
        self.backoffs += 1
        if self.backoffs >= self.max_backoffs_total:
            return None
        return 0


def retry_immediately(namespace: str | None = None) -> AbstractContextManager[None]:
    """
    Returns a contextmanager that prevents waits between retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not wait.
    """
    return replace_backoff_calculator(WaitLessBackoff, namespace=namespace)
