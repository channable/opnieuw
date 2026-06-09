from __future__ import annotations

from contextlib import _GeneratorContextManager

from .retries import BackoffCalculator, replace_backoff_calculator


class WaitLessBackoff(BackoffCalculator):
    def get_backoff(self) -> float | None:
        self.backoffs += 1
        if self.backoffs >= self.max_calls_total:
            return None
        return 0

# We have to use a private type from contextlib here, because otherwise we can't annotate
# that the return value is a context manager *and* can be called as a decorator.
#
# For more context see: https://github.com/python/typeshed/issues/6520
def retry_immediately(namespace: str | None = None) -> _GeneratorContextManager[None]:
    """
    Returns a contextmanager that prevents waits between retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not wait.
    """
    return replace_backoff_calculator(WaitLessBackoff, namespace=namespace)
