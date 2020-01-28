# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import time
import unittest

from opnieuw.clock import TestClock, MonotonicClock
from opnieuw.retries import RetryState, DoCall, retry


class TestRetryState(unittest.TestCase):
    def test_never_stop(self):
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

    def test_negative_time_value(self):
        try:
            self.clock.advance_to(-60.00)
        except AssertionError as e:
            self.assertIsInstance(e, AssertionError)
            self.assertEqual(self.clock.time, 0.0)

    def test_advanced_to(self):
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

    def test_raise_exception(self):
        try:
            self.foo()
        except TypeError as e:
            self.assertTrue(isinstance(e, TypeError))

    def test_retry_times(self):
        start = time.time()
        self.counter = 0

        try:
            self.foo()
        except TypeError as e:
            end = time.time()
            t_diff = end - start
            self.assertGreater(t_diff, 1)
            self.assertEqual(self.counter, 3)


if __name__ == "__main__":
    unittest.main()
