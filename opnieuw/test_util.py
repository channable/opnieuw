from contextlib import contextmanager
from typing import Iterator, Optional

from .retries import DoCall, RetryState, Action, __retry_state_namespaces


class ManualRetryState(RetryState):
    def __iter__(self) -> Iterator[Action]:
        for _ in range(self.max_calls_total):
            yield DoCall()


@contextmanager
def retry_immediately(namespace: Optional[str] = None) -> Iterator[None]:
    __retry_state_namespaces[namespace] = ManualRetryState
    try:
        yield
    finally:
        __retry_state_namespaces[namespace] = RetryState
