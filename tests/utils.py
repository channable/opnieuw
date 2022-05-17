import asyncio
import unittest
from contextlib import contextmanager
from typing import Iterator, Awaitable, TypeVar

T = TypeVar("T")


class AsyncTestCase(unittest.TestCase):
    """
    A very barebone TestCase that provides a utility to run an async event loop
    """

    @contextmanager
    def _new_loop(self) -> Iterator[asyncio.AbstractEventLoop]:
        policy = asyncio.get_event_loop_policy()
        loop = policy.new_event_loop()
        yield loop
        loop.close()

    def _run_async(self, fut: Awaitable[T]) -> T:
        with self._new_loop() as loop:
            return loop.run_until_complete(fut)
