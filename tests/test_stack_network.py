import helper

from monocle import _o
from monocle.callback import Callback
from monocle.stack import eventloop, network
from monocle.util import sleep

EOL = '\r\n'


class StackConnection(object):

    def __init__(self):
        self.buffer = ""
        self.is_closed = False
        self.is_reading = False
        self.read_cb = Callback()
        self.connect_cb = Callback()
        self.out = []
        self.disconnect_called = 0
        self.resume_called = 0

    def disconnect(self):
        self.disconnect_called += 1

    def closed(self):
        return self.is_closed

    def reading(self):
        return self.is_reading

    def resume(self):
        self.resume_called += 1

    def write(self, data):
        self.out.append(data)


class ConnectionTestCase(helper.TestCase):

    def setUp(self):
        self.stack_conn = StackConnection()
        self.conn = network.Connection(stack_conn=self.stack_conn)

    @property
    def buffer(self):
        return self.stack_conn.buffer

    @buffer.setter
    def buffer(self, value):
        self.stack_conn.buffer = value

    @helper.o
    def test(self):
        data = 'ok'
        self.buffer = data
        r = yield self.conn.read(2)
        self.assertEqual(r, data)
        self.assertEqual(self.buffer, '')
        self.assertEqual(self.stack_conn.resume_called, 0)

    @helper.o
    def test_read_delay(self):
        data = 'ok'
        self.buffer = 'o'
        self.conn.timeout = 0.2
        def populate():
            self.buffer += 'k'
            self.stack_conn.read_cb(None)
        eventloop.queue_task(0.1, populate)
        r = yield self.conn.read(2)
        self.assertEqual(r, data)
        self.assertEqual(self.stack_conn.resume_called, 1)
        yield sleep(0.2)  # ensure timeout has expired

    @helper.o
    def test_read_timeout(self):
        self.conn.timeout = 0.1
        try:
            yield self.conn.read(10)
        except network.ConnectionLost:
            pass
        else:
            raise Exception('ConnectionLost should be raised')
        self.assertEqual(self.stack_conn.resume_called, 1)

    @helper.o
    def test_read_some(self):
        data = 'ok'
        self.buffer = data
        r = yield self.conn.read_some()
        self.assertEqual(r, data)
        self.assertEqual(self.buffer, '')
        self.assertEqual(self.stack_conn.resume_called, 0)

    @helper.o
    def test_read_some_delay(self):
        data = 'ok'
        self.conn.timeout = 0.2
        def populate():
            self.buffer = data
            self.stack_conn.read_cb(None)
        eventloop.queue_task(0.1, populate)
        r = yield self.conn.read_some()
        self.assertEqual(r, data)
        self.assertEqual(self.stack_conn.resume_called, 1)
        yield sleep(0.2)  # ensure timeout has expired

    @helper.o
    def test_read_some_timeout(self):
        self.conn.timeout = 0.1
        try:
            yield self.conn.read_some()
        except network.ConnectionLost:
            pass
        else:
            raise Exception('ConnectionLost should be raised')
        self.assertEqual(self.stack_conn.resume_called, 1)

    @helper.o
    def test_read_util(self):
        data = 'hello.'
        self.buffer = 'hello.world'
        r = yield self.conn.read_until('.')
        self.assertEqual(r, data)
        self.assertEqual(self.buffer, 'world')
        self.assertEqual(self.stack_conn.resume_called, 0)

    @helper.o
    def test_readline(self):
        data = 'hello\n'
        self.buffer = 'hello\nworld'
        r = yield self.conn.readline()
        self.assertEqual(r, data)
        self.assertEqual(self.buffer, 'world')
        self.assertEqual(self.stack_conn.resume_called, 0)


class ClientServerTestCase(helper.TestCase):

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
                msg = yield conn.read_until(EOL)
            except network.ConnectionLost:
                break
            yield conn.write('you said: ' + msg.strip() + EOL)

    @helper.o
    def test_client(self):
        msg = 'ok'
        yield self.client.connect(helper.HOST, helper.PORT)
        yield self.client.write(msg + EOL)
        result = yield self.client.read_until(EOL)
        self.assertEqual(result, 'you said: ' + msg + EOL)
