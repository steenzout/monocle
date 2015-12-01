import sys

import monocle
from monocle import _o
monocle.init(sys.argv[1])

from monocle.stack import eventloop
from monocle.util import sleep

@_o
def sleeper_o(x, z=1):
    yield sleep(1)
    print x

def print_x(x, z=1):
    print x

@_o
def fail():
    raise Exception("whoo")
    yield sleep(1)

eventloop.queue_task(0, sleeper_o, x="oroutine worked")
eventloop.queue_task(0, print_x, x="function worked")
eventloop.queue_task(0, fail)
eventloop.run()
