# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

from opnieuw.retries import calculate_exponential_multiplier


def test_calculate_exponential_multiplier():
    expected_multiplier = 8.0
    multiplier = calculate_exponential_multiplier(5, 120)

    assert multiplier == expected_multiplier
