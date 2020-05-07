from contextlib import contextmanager
from typing import Iterator, Optional

from .retries import DoCall, RetryState, Action, __retry_state_namespaces


class WaitLessRetryState(RetryState):
    def __iter__(self) -> Iterator[Action]:
        for _ in range(self.max_calls_total):
            yield DoCall()


@contextmanager
def retry_immediately(namespace: Optional[str] = None) -> Iterator[None]:
    old_state = __retry_state_namespaces[namespace]
    __retry_state_namespaces[namespace] = WaitLessRetryState
    try:
        yield
    finally:
        __retry_state_namespaces[namespace] = old_state
