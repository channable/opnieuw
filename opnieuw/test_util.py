from typing import Iterator, Optional, ContextManager

from .retries import DoCall, RetryState, Action, replace_retry_state


class WaitLessRetryState(RetryState):
    def __iter__(self) -> Iterator[Action]:
        for _ in range(self.max_calls_total):
            yield DoCall()


def retry_immediately(namespace: Optional[str] = None) -> ContextManager[None]:
    """
    Contextmanager that prevents waits between retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not wait.
    """
    return replace_retry_state(WaitLessRetryState, namespace=namespace)
