from o_test import test
from contextlib import contextmanager

from monocle import _o, Return
from monocle.stack import network
from monocle.stack.network import http

import helper


@contextmanager
def http_server_running():
    @_o
    def handler(conn):
        data = 'Hello, World!'
        headers = http.HttpHeaders()
        headers.add('Content-Length', len(data))
        headers.add('Content-Type', 'text/plain')
        headers.add('Connection', 'close')
        yield Return(200, headers, data)
    service = http.HttpServer(helper.PORT, handler=handler)
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
    with http_server_running():
        with http_client() as client:
            yield client.connect(helper.HOST, helper.PORT)
            r = yield client.request('/')
            assert r.code == '200'  # should this be an int?
