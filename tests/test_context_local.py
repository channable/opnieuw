import asyncio
import threading
import time
import typing
import unittest
from collections import Counter

from opnieuw.retries import retry_async, retry
from opnieuw.test_util import retry_immediately
from opnieuw.util import no_retries
from tests.utils import AsyncTestCase


# The barriers are used to ensure all asyncio tasks/threads have their retry state modified
# even while the other asyncio tasks/threads are still running.
# Otherwise, one asyncio task/thread could finish and revert the retry state before the other starts.
# We want to test the retry state context during concurrency, so the flow should be:
#
#        T1         |       T2
# ------------------|------------------
# modify state      |
#                   | modify state
# wait for others   | wait for others
# perform test      | perform test
#                   |
# wait for others   | wait for others
# revert state      | revert state
#
# This ensures that if the retry state context is leaked across asyncio task or thread,
# the last one to modify the state will make the others' test fail.


class AsyncBarrier:
    def __init__(self, n: int) -> None:
        self.n = n
        self._current = 0
        self.event = asyncio.Event()

    async def wait(self) -> None:
        self._current += 1
        if self._current == self.n:
            self.event.set()
        await self.event.wait()


class TestAsyncContext(AsyncTestCase):
    counter: typing.Counter[str] = Counter()

    MAX_TOTAL_CALLS = 3

    @retry_async(
        retry_on_exceptions=TypeError,
        max_calls_total=MAX_TOTAL_CALLS,
        retry_window_after_first_call_in_seconds=3,
    )
    async def async_foo(self, counter_key: str) -> None:
        self.counter[counter_key] += 1
        # Yield control back to the event loop to give other coro a chance to run
        await asyncio.sleep(0)
        raise TypeError

    async def _retry_immediately_coro(
        self,
        start_barrier: AsyncBarrier,
        end_barrier: AsyncBarrier,
        counter_key: str = "retry_immediately",
    ) -> None:
        with retry_immediately():
            await start_barrier.wait()
            start = time.monotonic()
            try:
                await asyncio.wait_for(self.async_foo(counter_key), timeout=0.5)
            except TypeError:
                end = time.monotonic()
                runtime_seconds = end - start
                self.assertLess(runtime_seconds, 0.5)
                self.assertEqual(self.counter[counter_key], self.MAX_TOTAL_CALLS)
            finally:
                await end_barrier.wait()

    async def _no_retry_coro(
        self,
        start_barrier: AsyncBarrier,
        end_barrier: AsyncBarrier,
        counter_key: str = "no_retry",
    ) -> None:
        with no_retries():
            await start_barrier.wait()
            start = time.monotonic()
            try:
                await asyncio.wait_for(self.async_foo(counter_key), timeout=0.5)
            except TypeError:
                end = time.monotonic()
                runtime_seconds = end - start
                self.assertLess(runtime_seconds, 0.5)
                # We expect only one call since retries were disabled
                self.assertEqual(self.counter[counter_key], 1)
            finally:
                await end_barrier.wait()

    async def _no_retry_with_nested_immediately_retry_coro(
        self,
        start_barrier: AsyncBarrier,
        end_barrier: AsyncBarrier,
        counter_key: str = "no_retry_with_nested_retry_immediately",
    ) -> None:
        with no_retries():
            nested_task = asyncio.create_task(
                self._retry_immediately_coro(
                    start_barrier, end_barrier, counter_key="nested_retry_immediately"
                )
            )
            await start_barrier.wait()
            start = time.monotonic()
            try:
                await asyncio.wait_for(self.async_foo(counter_key), timeout=0.5)
                await nested_task
            except TypeError:
                end = time.monotonic()
                runtime_seconds = end - start
                self.assertLess(runtime_seconds, 0.5)
                # We expect only one call since retries were disabled
                self.assertEqual(self.counter[counter_key], 1)
            finally:
                await end_barrier.wait()

    def test_async_retry_state_context(self) -> None:
        """
        Test that the retry state is only modified in the context of an asyncio.Task
        and not globally.
        """

        async def _test_inner() -> None:
            self.counter = Counter()

            start_barrier = AsyncBarrier(2)
            end_barrier = AsyncBarrier(2)

            await asyncio.gather(
                self._no_retry_coro(start_barrier, end_barrier),
                self._retry_immediately_coro(start_barrier, end_barrier),
            )

            # retry state should not leak between tasks
            assert self.counter.most_common() == [
                ("retry_immediately", 3),
                ("no_retry", 1),
            ]

        self._run_async(_test_inner())

    def test_async_retry_state_context_nested(self) -> None:
        """
        Test that the retry state is only modified in the context of an asyncio.Task
        and not globally. In this case the tasks are nested.
        """

        async def _test_inner() -> None:
            self.counter = Counter()

            start_barrier = AsyncBarrier(2)
            end_barrier = AsyncBarrier(2)

            await self._no_retry_with_nested_immediately_retry_coro(
                start_barrier, end_barrier
            )

            # Nested task should be able to override retry state
            # without leaking into parent, and vice versa
            assert self.counter.most_common() == [
                ("nested_retry_immediately", 3),
                ("no_retry_with_nested_retry_immediately", 1),
            ]

        self._run_async(_test_inner())


class TestThreadedContext(unittest.TestCase):
    counter: typing.Counter[str] = Counter()

    @retry(
        retry_on_exceptions=TypeError,
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=3,
    )
    def foo(self, counter_key: str) -> None:
        self.counter[counter_key] += 1
        raise TypeError

    def test_threaded_retry_state_context(self) -> None:
        def _retry_immediately_inner(
            start_barrier: threading.Barrier, end_barrier: threading.Barrier
        ) -> None:
            counter_key = "retry_immediately"

            with retry_immediately():
                start_barrier.wait()
                start = time.monotonic()
                try:
                    self.foo(counter_key)
                except TypeError:
                    end = time.monotonic()
                    runtime_seconds = end - start
                    self.assertLess(runtime_seconds, 0.5)
                    self.assertEqual(self.counter[counter_key], 3)
                finally:
                    end_barrier.wait()

        def _no_retry_inner(
            start_barrier: threading.Barrier, end_barrier: threading.Barrier
        ) -> None:
            counter_key = "no_retry"

            with no_retries():
                start_barrier.wait()
                start = time.monotonic()
                try:
                    self.foo(counter_key)
                except TypeError:
                    end = time.monotonic()
                    runtime_seconds = end - start
                    self.assertLess(runtime_seconds, 0.5)
                    self.assertEqual(self.counter[counter_key], 1)
                finally:
                    end_barrier.wait()

        self.counter = Counter()
        start_barrier = threading.Barrier(2)
        end_barrier = threading.Barrier(2)
        threads = [
            threading.Thread(target=_no_retry_inner, args=(start_barrier, end_barrier)),
            threading.Thread(
                target=_retry_immediately_inner, args=(start_barrier, end_barrier)
            ),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # retry state should not leak between threads
        assert self.counter.most_common() == [
            ("retry_immediately", 3),
            ("no_retry", 1),
        ]


if __name__ == "__main__":
    unittest.main()
