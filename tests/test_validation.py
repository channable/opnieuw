# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import unittest
from opnieuw import retry, retry_async


class TestParameterValidation(unittest.TestCase):
    def test_invalid_max_calls_total_1(self) -> None:
        with self.assertWarnsRegex(UserWarning, "`max_calls_total` should at least be 2"):
            retry(retry_on_exceptions=(ValueError,), max_calls_total=1)

        with self.assertWarnsRegex(UserWarning, "`max_calls_total` should at least be 2"):
            retry_async(retry_on_exceptions=(ValueError,), max_calls_total=1)

    def test_invalid_max_calls_total_0(self) -> None:
        with self.assertWarnsRegex(UserWarning, "`max_calls_total` should at least be 2"):
            retry(retry_on_exceptions=(ValueError,), max_calls_total=0)

        with self.assertWarnsRegex(UserWarning, "`max_calls_total` should at least be 2"):
            retry_async(retry_on_exceptions=(ValueError,), max_calls_total=0)

    def test_negative_retry_window(self) -> None:
        with self.assertWarnsRegex(
            UserWarning,
            "`retry_window_after_first_call_in_seconds` must be non-negative",
        ):
            retry(
                retry_on_exceptions=(ValueError,),
                max_calls_total=3,
                retry_window_after_first_call_in_seconds=-1,
            )

        with self.assertWarnsRegex(
            UserWarning,
            "`retry_window_after_first_call_in_seconds` must be non-negative",
        ):
            retry_async(
                retry_on_exceptions=(ValueError,),
                max_calls_total=3,
                retry_window_after_first_call_in_seconds=-1,
            )



if __name__ == "__main__":
    unittest.main()
