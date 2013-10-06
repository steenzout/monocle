import helper

from collections import deque
from monocle import experimental


class ChannelTestCase(helper.TestCase):

    def setUp(self):
        self.bufsize = 2
        self.ch = experimental.Channel(self.bufsize)

    @helper.o
    def test_send_recv(self):
        for x in range(2):
            yield self.ch.send('ok%s' % x)
        for x in range(2):
            r = yield self.ch.recv()
            self.assertEqual(r, 'ok%s' % x)
