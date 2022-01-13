"""Tests for the logging module."""
from mxxn.logging import logger


class TestLogger(object):
    """Test for looger function."""

    def test_context_added(self, tmp_path, caplog):
        """The context was added to the logger name."""
        log = logger('some_context')
        log.error('test error')

        assert caplog.records[-1].msg == 'test error'
        assert caplog.records[-1].name == 'mixxin.mxxn.some_context'
        assert caplog.records[-1].levelname == 'ERROR'
