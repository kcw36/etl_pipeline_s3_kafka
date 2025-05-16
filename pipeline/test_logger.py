# pylint:skip-file
"""Tests for logger module."""

from unittest.mock import patch
from pytest import mark
from logging import StreamHandler, FileHandler

from logger import get_logger


@mark.parametrize("streaming, types", ((True, [StreamHandler, FileHandler]), (False, [StreamHandler])))
def test_get_logger_valid(streaming, types):
    """Test that get logger creates a logger with expected handlers."""
    handlers = get_logger(streaming).handlers
    for handler in handlers:
        assert type(handler) in types
