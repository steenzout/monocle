"""Logger for monocle."""
# -*- coding: utf-8 -*-

import sys

import logging

from monocle.core import format_tb


def get(name=None):
    """
    Return a monocle logger adapter with the specified name, creating it if necessary.

    If no name is specified, return a root logger adapter.

    :param name: logger name.
    :return: monocle logger adapter.
    """
    return Adapter(logging.getLogger(name))


class Adapter(logging.LoggerAdapter):

    """A monocle-friendly logger."""

    def __init__(self, logger):
        """
        Initialize a LoggerAdapter instance.

        :param logger: the logger instance.
        """
        super(Adapter, self).__init__(logger, None)

    def exception(self, msg, *args, **kwargs):
        """
        Handle an exception call.

        In case of o-routines,
        this function will write to this adapter's logger
        the exception message with its stack trace.
        Otherwise, it will delegate the log message processing to the underlying logger.
        """
        ex = sys.exc_info()[1]

        if hasattr(ex, '_monocle'):
            self.logger.error('%s\n%s', msg, format_tb(ex))
        else:
            super(Adapter, self).exception(msg, *args, **kwargs)
