import helper

import monocle
from monocle import core


class ReturnTestCase(helper.TestCase):

    def test_none(self):
        r = core.Return()
        self.assertEqual(r.value, None)

    def test_single(self):
        r = core.Return('ok')
        self.assertEqual(r.value, 'ok')

    def test_multi(self):
        r = core.Return('one', 'two')
        self.assertEqual(r.value, ('one', 'two'))
