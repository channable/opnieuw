from typing import Iterator, Optional, ContextManager

from .retries import DoCall, RetryState, Action, replace_retry_state


class NoRetryState(RetryState):
    def __iter__(self) -> Iterator[Action]:
        yield DoCall()


def no_retries(namespace: Optional[str] = None) -> ContextManager[None]:
    """
    Contextmanager that disables retries for all `retry` and
    `retry_async` decorators with the provided namespace. None means all decorators
    without a provided namespace will not retry.
    """
    return replace_retry_state(NoRetryState, namespace=namespace)
