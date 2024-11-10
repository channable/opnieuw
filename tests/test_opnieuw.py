# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import random
import time
import unittest
import warnings
from unittest import mock

from opnieuw.clock import DummyClock, MonotonicClock
from opnieuw.retries import BackoffCalculator, retry, retry_async
from opnieuw.test_util import retry_immediately


def should_retry(ex: Exception) -> bool:
    return "Please try again" in str(ex)


class TestBackoffCalculator(unittest.TestCase):
    def test_max_calls_is_zero(self) -> None:
        retry_state = BackoffCalculator(
            MonotonicClock(),
            max_calls_total=0,
            retry_window_after_first_call_in_seconds=3,
        )

        # This kind of BackoffCalculator should only return None
        self.assertEqual(None, retry_state.get_backoff())


class TestRetryClock(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = DummyClock()

    def test_negative_time_value(self) -> None:
        try:
            self.clock.advance_to(-60.00)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
            self.assertEqual(self.clock.time, 0.0)

    def test_advanced_to(self) -> None:
        self.clock.advance_to(60.00)
        self.assertEqual(self.clock.time, 60.00)


class TestRetryDecorator(unittest.TestCase):
    counter = 0

    def error(self, kind=None) -> None:
        self.counter += 1
        raise kind if kind else Exception("Please try again"
                                          if self.counter > 0 and self.counter % 2 == 0
                                          else "Skip all retries")

    @retry(
        retry_on_exceptions=TypeError,
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=3,
    )
    def foo(self) -> None:
        return self.error(TypeError)

    @retry(
        retry_on_exceptions=should_retry,
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=3
    )
    def bar(self) -> None:
        return self.error()

    @retry(
        retry_on_exceptions=(TypeError, ValueError),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=3
    )
    def foobar(self, ex: Exception = TypeError) -> None:
        return self.error(ex)

    @retry(
        retry_on_exceptions=(TypeError, ValueError, should_retry),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=3
    )
    def barfoo(self, kind=None) -> None:
        return self.error(kind)

    def test_raise_exception(self) -> None:
        try:
            self.foo()
        except Exception as e:
            self.assertTrue(isinstance(e, TypeError))

    def test_raise_multiple_exceptions(self) -> None:
        with retry_immediately():
            try:
                self.foobar(IndexError)
            except Exception as e:
                self.assertLess(self.counter, 3)
                self.assertTrue(isinstance(e, IndexError))

            try:
                self.counter = 0
                self.foobar(ValueError)
            except Exception as e:
                self.assertGreaterEqual(self.counter, 3)
                self.assertTrue(isinstance(e, ValueError))

    def _retry_with_waits(self) -> None:
        self.counter = 0

        try:
            self.foo()
        except TypeError:
            self.assertEqual(self.counter, 3)

    def test_retry_with_callable(self) -> None:
        try:
            self.bar()
        except Exception as e:
            self.assertEqual(str(e), "Skip all retries")

    def test_retry_with_mixed_callable(self) -> None:
        with retry_immediately():
            try:
                self.barfoo()
            except Exception as e:
                self.assertLessEqual(self.counter, 3)
                self.assertTrue(isinstance(e, Exception))

            try:
                self.counter = 0
                self.barfoo(ValueError)
            except Exception as e:
                self.assertGreaterEqual(self.counter, 3)
                self.assertTrue(isinstance(e, ValueError))

            try:
                self.counter = 0
                self.barfoo(TypeError)
            except Exception as e:
                self.assertGreaterEqual(self.counter, 3)

    @mock.patch.object(random, "uniform", return_value=0.1)
    def test_retry_with_waits(self, mocked_random) -> None:
        self._retry_with_waits()
        mocked_random.assert_called()

    def test_retry_immediately_global(self) -> None:
        start = time.monotonic()
        self.counter = 0
        with retry_immediately():
            try:
                self.foo()
            except TypeError as e:
                end = time.monotonic()
                runtime_seconds = end - start
                self.assertLess(runtime_seconds, 0.5)
                self.assertEqual(self.counter, 3)

    @retry(
        retry_on_exceptions=ValueError,
        max_calls_total=60,
        retry_window_after_first_call_in_seconds=120,
        namespace="bar_retry",
    )
    def namespaced_retry_foo(self) -> None:
        self.counter += 1
        raise ValueError

    def test_retry_immediately(self) -> None:
        start = time.monotonic()
        self.counter = 0
        with retry_immediately("bar_retry"):
            try:
                self.namespaced_retry_foo()

            except ValueError as e:
                end = time.monotonic()
                runtime_seconds = end - start
                self.assertLess(runtime_seconds, 1)
                self.assertEqual(self.counter, 60)

    @mock.patch.object(random, "uniform", return_value=0.1)
    def test_mixed_states(self, mocked_random) -> None:
        with retry_immediately():
            self._retry_with_waits()
            mocked_random.assert_not_called()
        with retry_immediately("bar_retry"):
            self._retry_with_waits()
            mocked_random.assert_called()


class TestExceptionChaining(unittest.TestCase):
    def setUp(self) -> None:
        self.counter = 0

    @retry(
        retry_on_exceptions=(TypeError, ValueError),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=1,
    )
    def raise_depending_on_counter(self) -> None:
        self.counter += 1
        if self.counter == 1:
            raise TypeError
        elif self.counter == 2:
            raise ValueError
        else:
            raise IndexError

    def test_exception_chaining(self) -> None:
        with retry_immediately():
            try:
                self.raise_depending_on_counter()
            except IndexError as e:
                self.assertIsInstance(e.__cause__, ValueError)
                assert e.__cause__ is not None
                self.assertIsInstance(e.__cause__.__cause__, TypeError)


class TestWarningOnOneRetry(unittest.TestCase):
    def test_raise_warning_for_retry_once(self) -> None:
        """Test that a UserWarning is raised for non-sensical max_calls_total values."""

        with warnings.catch_warnings(record=True) as w:

            @retry(retry_on_exceptions=ValueError, max_calls_total=1)
            def func() -> None:
                ...

            warnings.simplefilter("always")
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "max_calls_total" in str(w[-1].message)

        with warnings.catch_warnings(record=True) as w:

            @retry_async(retry_on_exceptions=ValueError, max_calls_total=1)
            async def func() -> None:
                ...

            warnings.simplefilter("always")
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "max_calls_total" in str(w[-1].message)


if __name__ == "__main__":
    unittest.main()
