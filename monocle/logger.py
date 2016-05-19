# -*- coding: utf-8 -*-

import sys

import logging

from monocle.core import format_tb


class Adapter(logging.LoggerAdapter):
    """
    A monocle-friendly logger.
    """

    def __init__(self, logger):
        """
        Initializes a LoggerAdapter instance.

        :param logger: the logger instance.
        """
        super(Adapter, self).__init__(logger, None)

    def exception(self, msg, *args, **kwargs):
        """
        Delegate an exception call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        e = sys.exc_info()[1]

        if hasattr(e, '_monocle'):
            self.logger.error('%s\n%s', msg, format_tb(e))
        else:
            super(Adapter, self).exception(msg, *args, **kwargs)
