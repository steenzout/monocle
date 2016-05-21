# -*- coding: utf-8 -*-

import logging
import monocle
import unittest

from monocle import _o
from monocle.logging import get, Adapter
from monocle.stack import eventloop

from testfixtures import LogCapture


class GetTestCase(unittest.TestCase):

    """Tests for the monocle.logger.get() function."""

    def test_get(self):
        """Test get without logger name."""
        adapter = get()
        self.assertIsNotNone(adapter)
        self.assertEqual('root', adapter.logger.name)

    def test_get_with_name(self):
        """Test get with logger name."""
        adapter = get('logger_test')
        self.assertIsNotNone(adapter)
        self.assertEqual('logger_test', adapter.logger.name)


class AdapterTestCase(unittest.TestCase):

    """Tests for the monocle.logger.Adapter class."""

    def setUp(self):
        """
        Setup log capture and monocle logger adapter instance.
        """
        self.l = LogCapture()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = Adapter(logger)

    def tearDown(self):
        """
        Tear down log capture.
        """
        self.l.uninstall()

    def test_exception_outside_o(self):
        """
        Test behavior of monocle.logger.LoggerAdapter.exception() function when
        used outside of an o-routine.
        """

        try:
            raise Exception('Test')
        except Exception as e:
            self.logger.exception(e)

        self.l.check(('root', 'ERROR', 'Test'))

    def test_exception_inside_o(self):
        """
        Test behavior of monocle.logger.LoggerAdapter.exception() function when
        used inside of an o-routine.
        """
        @_o
        def t():
            @_o
            def e():
                raise Exception('Test')

            try:
                _ = yield e()
            except BaseException as e:
                self.logger.exception('%s %s', 'unexpected error', e)
                raise e
            finally:
                eventloop.halt()

        monocle.launch(t)
        eventloop.run()

        stack_trace = '\nTraceback (most recent call last):\n  File '
        self.assertEqual(2, len([x for x in self.l.actual()]))

        found_root = False
        found_monocle = False
        for name, level, message in self.l.actual():
            self.assertEqual('ERROR', level)
            if name == 'root':
                self.assertTrue(message.startswith('%s%s' % ('unexpected error Test', stack_trace)))
                found_root = True
            elif name == 'monocle':
                # monocle logger does not log the exception message
                self.assertTrue(message.startswith('%s%s' % ('', stack_trace)))
                found_monocle = True

        self.assertTrue(found_root)
        self.assertTrue(found_monocle)
