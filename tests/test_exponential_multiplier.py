from retry.retries import calculate_exponential_multiplier


def test_calculate_exponential_multiplier():
	expected_multiplier = 8.0
	multiplier = calculate_exponential_multiplier(5, 120)

	assert multiplier == expected_multiplier


