# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

# pylint: disable=raising-bad-type

from __future__ import annotations

import asyncio
import functools
import logging
import random
import sys
import time
from collections import defaultdict
from collections.abc import Callable, Coroutine, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import TypeVar

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

from .clock import Clock, MonotonicClock

logger = logging.getLogger(__name__)

R = TypeVar("R")
P = ParamSpec("P")


def calculate_exponential_multiplier(
    max_calls_total: int, retry_window_after_first_call_in_seconds: int
) -> float:
    r"""
    Solve the following equation for `m`:
        \sum_{k=0}^{n} m 2^k = <retry_window_after_first_call_in_seconds>

    where `n` is the number of attempts. Since we start at `k=0`, then
    `n = max_calls_total - 2`.

    An example:
        Let `max_calls_total = 4` and `retry_window_after_first_call_in_seconds = 120`,
        then we have:
            \sum_{k=0}^{4 - 2} m 2^k = 120

        which expands into:
            m * 2^0 + m * 2^1 + m * 2^2 = 120
            m + 2m + 4m = 120
            7m = 120
            m = 120 / 7

    If we take a partial sum of this geometric sequence, we can simplify the equation:
        \sum_{k=0}^{n-1} 2^k ≈ 2^{max_calls_total - 1} - 1

    Using the example from above, we have:
        2^{4 - 1} -1 = 7

        ∴ 7m = 120 => m = 120 / 7
    """

    count = 2.0 ** (max_calls_total - 1) - 1
    multiplier = retry_window_after_first_call_in_seconds / max(count, 1)

    return multiplier


class WaitState:
    """
    Calculate how often and how long to wait depending on input parameters.
    """

    def __init__(
        self,
        clock: Clock,
        max_calls_total: int,
        retry_window_after_first_call_in_seconds: int,
    ) -> None:
        self.clock = clock
        self.max_calls_total = max_calls_total
        self.deadline_second = (
            self.clock.seconds_since_epoch() + retry_window_after_first_call_in_seconds
        )

        self.base_in_seconds = calculate_exponential_multiplier(
            max_calls_total, retry_window_after_first_call_in_seconds
        )
        self.waits = 0

    def get_seconds_to_wait(self) -> float | None:
        """
        Return the amount of seconds to wait before a next call.

        None indicates that there should be no more waits.
        """
        # The number of waits is always one less than the amount of calls since the first call
        # isn't included.
        if self.waits + 1 >= self.max_calls_total:
            logger.debug(f"Used up all {self.max_calls_total} retries.")
            return None

        wait_seconds = self.base_in_seconds * 2**self.waits
        jittered_wait = random.uniform(0.0, wait_seconds)

        self.waits += 1
        if jittered_wait > self.deadline_second - self.clock.seconds_since_epoch():
            logger.debug("Next attempt would be after retry deadline, not retrying.")
            return None

        logger.debug(
            f"Sleep for {jittered_wait:.3f} seconds after attempt {self.waits}"
        )
        return jittered_wait


__wait_state_namespaces: dict[str | None, ContextVar[type[WaitState]]] = defaultdict(
    lambda: ContextVar("opnieuw_default_retry_state", default=WaitState)
)


def _get_wait_state_class(namespace: str | None) -> type[WaitState]:
    return __wait_state_namespaces[namespace].get()


@contextmanager
def replace_wait_state(
    state: type[WaitState], *, namespace: str | None = None
) -> Iterator[None]:
    """
    A context manager that replaces the state of the specified namespace with the
    given `WaitState`.
    This can be useful to customize the retry behavior, such as disabling the sleep interval during
    tests (see `opnieuw.test_util.retry_immediately`).

    Note: the wait state is context-local, meaning that changing the state in a thread or
    asyncio task will not bleed to other threads or asyncio tasks.
    See https://docs.python.org/3/library/contextvars.html for more details.
    """
    token = __wait_state_namespaces[namespace].set(state)
    try:
        yield
    finally:
        __wait_state_namespaces[namespace].reset(token)


def retry(
    *,
    retry_on_exceptions: type[Exception] | tuple[type[Exception], ...],
    max_calls_total: int = 3,
    retry_window_after_first_call_in_seconds: int = 60,
    namespace: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Retry a function using a Full Jitter exponential backoff.

    This function exposes four settings:

     - `retry_on_exceptions` - A tuple of exception types to retry on.
     - `max_calls_total` - The maximum number of calls of the decorated
       function, in total. Includes the initial call and all retries.
     - `retry_window_after_first_call_in_seconds` - The number of seconds to
       spread out the retries over after the first call.
     - `namespace` - A name with which the wait behavior can be controlled
       using the `opnieuw.test_util.retry_immediately` contextmanager.

    This function will:

     - Calculate how to fit `max_calls_total` executions of function in the
       retry window with exponential backoff and jitter.
     - Call the decorated function until it either succeeds or the retry window
       is over.

    This function will NOT:

     - Time the execution of the decorated function. It assumes its execution
       is instant.
     - Interrupt execution of the decorated function once the retry window is
       over.
     - Guarantee that `max_calls_total` is actually reached. Once the retry
       window is over, no new calls will be made. Once the function executes
       successfully, no new calls will be made.
     - Guarantee that `retry_window_after_first_call_seconds` have passed after
       `max_calls_total` have been made. The expected time is after `0.5 *
       retry_window_after_first_call`. The actual wait time is sampled
       uniformly from [0, base_delay * 2 ^ i], which has an expected value of
       half the size of the interval.

    You can read this code as:

        @retry(
            retry_on_exceptions=(FooError, SomeOtherError),
            max_calls_total=3,
            retry_window_after_first_call_in_seconds=60,
        )
        def foo() -> None:
            pass

    Call `foo()` at most 3 times. If `foo()` raises either `FooError`, or
    `SomeOtherError` attempt 2 more times over a period of 60 seconds. If 60
    seconds have elapsed after the first retry, the second retry is not
    scheduled.

    Opnieuw is based on a retry algorithm off of:
        https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    """

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(f)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            wait_state = _get_wait_state_class(namespace)(
                MonotonicClock(),
                max_calls_total=max_calls_total,
                retry_window_after_first_call_in_seconds=retry_window_after_first_call_in_seconds,
            )
            while True:
                try:
                    return f(*args, **kwargs)
                except retry_on_exceptions as e:
                    last_exception = e

                    sleep_seconds = wait_state.get_seconds_to_wait()
                    if sleep_seconds is None:
                        raise last_exception

                    time.sleep(sleep_seconds)

        return wrapper

    return decorator


def retry_async(
    *,
    retry_on_exceptions: type[Exception] | tuple[type[Exception], ...],
    max_calls_total: int = 3,
    retry_window_after_first_call_in_seconds: int = 60,
    namespace: str | None = None,
) -> Callable[
    [Callable[P, Coroutine[None, None, R]]], Callable[P, Coroutine[None, None, R]]
]:
    def decorator(
        f: Callable[P, Coroutine[None, None, R]]
    ) -> Callable[P, Coroutine[None, None, R]]:
        @functools.wraps(f)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            wait_state = _get_wait_state_class(namespace)(
                MonotonicClock(),
                max_calls_total=max_calls_total,
                retry_window_after_first_call_in_seconds=retry_window_after_first_call_in_seconds,
            )

            while True:
                try:
                    return await f(*args, **kwargs)
                except retry_on_exceptions as e:
                    last_exception = e

                    sleep_seconds = wait_state.get_seconds_to_wait()
                    if sleep_seconds is None:
                        raise last_exception

                    await asyncio.sleep(sleep_seconds)

        return wrapper

    return decorator


retry_async.__doc__ = retry.__doc__
