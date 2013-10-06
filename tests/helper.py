import functools
import os

INIT = os.environ.get('BACKEND', 'twisted')
HOST = '127.0.0.1'
PORT = 5555

import monocle
monocle.init(INIT)

from monocle.twisted_stack.utils import cb_to_df
from twisted.trial.unittest import TestCase

def o(f):
    oroutine = monocle._o(f)
    return functools.update_wrapper(
        lambda *a, **k: cb_to_df(oroutine(*a, **k)), oroutine)
