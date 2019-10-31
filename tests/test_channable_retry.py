import unittest


class TestRetryState(unittest.TestCase):

    def test_never_stop(self):
        r = Retrying()
        self.assertFalse(r.stop(3, 6546))

    def test_stop_after_attempt(self):
        r = Retrying(stop_max_attempt_number=3)
        self.assertFalse(r.stop(2, 6546))
        self.assertTrue(r.stop(3, 6546))
        self.assertTrue(r.stop(4, 6546))


class TestClock(unittest.TestCase):
    pass


class TestChannableRetryDecorator(unittest.TestCase):

    def test_no_sleep(self):
        r = Retrying()
        self.assertEqual(0, r.wait(18, 9879))

    def test_fixed_sleep(self):
        r = Retrying(wait_fixed=1000)
        self.assertEqual(1000, r.wait(12, 6546))


@retry(wait_fixed=50, retry_on_result=retry_if_result_none)
def _retryable_test_with_wait(thing):
    return thing.go()


class TestAsyncRetryDecorator(unittest.TestCase):

    def test_with_wait(self):
        start = current_time_ms()
        result = _retryable_test_with_wait(NoneReturnUntilAfterCount(5))
        t = current_time_ms() - start
        self.assertTrue(t >= 250)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
