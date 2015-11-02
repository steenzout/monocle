from o_test import test
from contextlib import contextmanager

from monocle import _o, Return
from monocle.stack import network
from monocle.stack.network import http


@contextmanager
def http_server_running(port):
    @_o
    def handler(conn):
        data = 'Hello, World!'
        headers = http.HttpHeaders()
        headers.add('Content-Length', len(data))
        headers.add('Content-Type', 'text/plain')
        headers.add('Connection', 'close')
        yield Return(200, headers, data)
    service = http.HttpServer(port, handler=handler)
    network.add_service(service)
    try:
        yield
    finally:
        service.stop()


@contextmanager
def http_client():
    client = http.HttpClient()
    try:
        yield client
    finally:
        client.close()


@test
@_o
def test_client():
    addr = '127.0.0.1'
    port = 5556
    with http_server_running(port):
        with http_client() as client:
            yield client.connect(addr, port)
            r = yield client.request('/')
            assert r.code == '200'  # should this be an int?
