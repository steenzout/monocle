import helper

from monocle import _o
from monocle.stack import network


class ClientServerTestCase(helper.TestCase):
    EOL = '\r\n'

    def setUp(self):
        self.client = network.Client()
        self.service = network.Service(self.handler, bindaddr=helper.HOST, port=helper.PORT)
        network.add_service(self.service)

    def tearDown(self):
        try:
            self.client.close()
        except:
            pass
        try:
            self.service.stop()
        except:
            pass
        helper.TestCase.tearDown(self)

    @_o
    def handler(self, conn):
        while True:
            try:
                msg = yield conn.read_until(self.EOL)
            except network.ConnectionLost:
                break
            yield conn.write('you said: ' + msg.strip() + self.EOL)

    @helper.o
    def test_client(self):
        msg = 'ok'
        yield self.client.connect(helper.HOST, helper.PORT)
        yield self.client.write(msg + self.EOL)
        result = yield self.client.read_until(self.EOL)
        self.assertEqual(result, 'you said: ' + msg + self.EOL)
