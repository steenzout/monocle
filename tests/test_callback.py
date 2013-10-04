import helper

from monocle import callback


class TestCase(helper.TestCase):

    def setUp(self):
        self.calls = []

    def call(self, result):
        self.calls.append(result)


class CallbackTestCase(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.cb = callback.Callback()

    def test_result(self):
        self.assertFalse(hasattr(self.cb, 'result'))
        self.cb('ok')
        self.assertEqual(self.cb.result, 'ok')

    def test_add(self):
        self.assertEqual(self.cb._handlers, [])
        self.cb.add(self.call)
        self.assertEqual(self.cb._handlers, [self.cb])
        self.assertRaises(TypeError, cb.add, False)
        self.assertEqual(self.cb._handlers, [self.cb])
        self.assertEqual(self.calls, [])
        self.cb('ok')
        self.assertEqual(self.calls, ['ok'])
        cb.add(self.call)
        self.assertEqual(self.calls, ['ok', 'ok'])
        self.assertRaises(TypeError, cb.add, False)


class DeferTestCase(TestCase):

    def test_callback(self):
        cb = callback.defer('ok')
        self.assertTrue(isinstance(cb, callback.Callback))
        self.assertEqual(cb.result, 'ok')
        self.assertEqual(self.calls, [])
        cb.add(self.call)
        self.assertEqual(self.calls, ['ok'])
