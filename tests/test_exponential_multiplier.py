# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import unittest

from opnieuw.retries import calculate_exponential_multiplier


class ExponentialMultiplierTests(unittest.TestCase):
    def test_calculate_exponential_multiplier(self):
        expected_multiplier = 8.0
        multiplier = calculate_exponential_multiplier(5, 120)

        self.assertEqual(multiplier, expected_multiplier)


if __name__ == "__main__":
    unittest.main()
