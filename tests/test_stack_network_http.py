import helper

from monocle import _o, Return
from monocle.stack import network
from monocle.stack.network import http


class ClientServerTestCase(helper.TestCase):
    EOL = '\r\n'

    def setUp(self):
        self.client = http.HttpClient()
        self.service = http.HttpServer(helper.PORT, handler=self.handler)
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
        data = 'Hello, World!'
        headers = http.HttpHeaders()
        headers.add('Content-Length', len(data))
        headers.add('Content-Type', 'text/plain')
        headers.add('Connection', 'close')
        yield Return(200, headers, data)

    @helper.o
    def test_client(self):
        yield self.client.connect(helper.HOST, helper.PORT)
        r = yield self.client.request('/')
        self.assertEqual(r.code, '200')  # should this be an int?
