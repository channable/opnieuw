# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import unittest

from opnieuw.retries import calculate_exponential_multiplier


class ExponentialMultiplierTests(unittest.TestCase):
    def test_calculate_exponential_multiplier(self):
        # test for max_calls_total=1 and 2
        expected_multiplier = 120.0
        multiplier = calculate_exponential_multiplier(1, 120)
        self.assertEqual(multiplier, expected_multiplier)

        multiplier = calculate_exponential_multiplier(2, 120)
        self.assertEqual(multiplier, expected_multiplier)

        # test max_calls_total > 2
        expected_multiplier = 8.0
        multiplier = calculate_exponential_multiplier(5, 120)

        self.assertEqual(multiplier, expected_multiplier)


if __name__ == "__main__":
    unittest.main()
