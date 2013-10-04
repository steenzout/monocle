import helper

import time
from monocle import util


class SleepTestCase(helper.TestCase):

    @helper.o
    def test_simple(self):
        t = time.time()
        yield util.sleep(0.01)
        dt = time.time() - t
        self.assertTrue(dt > 0.005 and dt < 0.015)
