# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import time
import unittest

from opnieuw.clock import TestClock, MonotonicClock
from opnieuw.retries import RetryState, DoCall, retry
from opnieuw.test_util import retry_immediately
from opnieuw.exceptions import BackoffAndRetryException


class CustomBackoffThrottleError(BackoffAndRetryException):
    pass


class TestRetryState(unittest.TestCase):
    def test_never_stop(self) -> None:
        retry_state = RetryState(
            MonotonicClock(),
            max_calls_total=0,
            retry_window_after_first_call_in_seconds=3,
        )

        for rt in retry_state:
            self.assertIsInstance(rt, DoCall)


class TestRetryClock(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = TestClock()

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

    @retry(
        retry_on_exceptions=TypeError,
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=3,
    )
    def foo(self) -> None:
        self.counter += 1
        raise TypeError

    def test_raise_exception(self) -> None:
        try:
            self.foo()
        except Exception as e:
            self.assertTrue(isinstance(e, TypeError))

    def test_retry_with_waits(self) -> None:
        start = time.monotonic()
        self.counter = 0

        try:
            self.foo()
        except TypeError as e:
            end = time.monotonic()
            runtime_seconds = end - start
            self.assertGreater(runtime_seconds, 0.5)
            self.assertEqual(self.counter, 3)

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

    def test_mixed_states(self) -> None:
        with retry_immediately():
            self.assertRaises(AssertionError, self.test_retry_with_waits)
        with retry_immediately("bar_retry"):
            self.test_retry_with_waits()

    @retry(
        retry_on_exceptions=ValueError,
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=10,
    )
    def namespaced_retry_fixed_backoff(self) -> None:
        self.counter += 1
        if self.counter == 4:
            raise CustomBackoffThrottleError(seconds=1)
        raise ValueError

    def test_fixed_backoff_reset_max_calls(self):
        self.counter = 0
        start = time.monotonic()

        with retry_immediately():
            self.assertRaises(ValueError, self.namespaced_retry_fixed_backoff)

        # expect to sleep at least 1 second for the BackoffAndRetry
        end = time.monotonic()
        runtime_seconds = end - start
        self.assertGreater(runtime_seconds, 1)

        # we exhaust max_calls_total twice
        assert self.counter == 8


if __name__ == "__main__":
    unittest.main()
