"""Logger for monocle."""
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

import logging

from monocle.core import format_tb


def getLogger(name=None):
    """
    Return a monocle logger adapter with the specified name, creating it if necessary.

    If no name is specified, return a root logger adapter.

    :param name: logger name.
    :return: monocle logger adapter.
    """
    return Adapter(logging.getLogger(name), None)


class Adapter(logging.LoggerAdapter):

    """A monocle-friendly logger."""

    def exception(self, msg, *args, **kwargs):
        """
        Handle an exception call.

        Exceptions thrown from o-routines contain extra metadata to allow us to
        reconstruct a traceback that follows the stack through
        the round trips to the event loop that happen at every yield in an o-routine.
        """
        ex = sys.exc_info()[1]

        if hasattr(ex, '_monocle'):
            args = args + (format_tb(ex),)
            self.logger.error('%s\n%%s' % msg, *args, **kwargs)
        else:
            super(Adapter, self).exception(msg, *args, **kwargs)
