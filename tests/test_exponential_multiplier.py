import unittest

from retry.utils import calculate_exponential_multiplier


def test_calculate_exponential_multiplier():
	expected_multiplier = 8.0
	multiplier = calculate_exponential_multiplier(5, 120)
   	
   	assert 	multi == expected_multiplier


def test_exponential_with_max_wait_and_multiplier(self):
	r = Retrying(wait_exponential_max=50000, wait_exponential_multiplier=1000)
	self.assertEqual(r.wait(1, 0), 2000)
	self.assertEqual(r.wait(2, 0), 4000)
	self.assertEqual(r.wait(3, 0), 8000)
	self.assertEqual(r.wait(4, 0), 16000)
	self.assertEqual(r.wait(5, 0), 32000)
	self.assertEqual(r.wait(6, 0), 50000)
	self.assertEqual(r.wait(7, 0), 50000)
	self.assertEqual(r.wait(50, 0), 50000)
