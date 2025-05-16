# pylint:skip-file
"""Tests for pipeline script."""

from unittest.mock import patch, Mock
from pytest import mark

from consumer import (get_message_data,
                      is_valid_message,
                      log_message)


def test_log_message_valid():
    """Test log message logs the correct message."""
    message = '{"at": "2025-05-14T12:33:35.076377+01:00", "site": "5", "val": 3}'
    log_prefix = "MESSAGE: %s"
    mock_message = Mock()
    mock_message.value.return_value = message.encode()
    with patch("consumer.is_valid_message") as v, patch("consumer.logging.getLogger") as mock_get_logger:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance
        v.return_value = (True, "")
        log_message(mock_message)
        mock_logger_instance.info.assert_called_with(log_prefix, message)


def test_log_message_invalid():
    """Test log message logs the correct error message."""
    message = '{"site": "5", "val": 3}'
    log_prefix = "INVALID: %s, with ERROR: %s"
    error = "No 'at' key"
    mock_message = Mock()
    mock_message.value.return_value = message.encode()
    with patch("consumer.is_valid_message") as v, patch("consumer.logging.getLogger") as mock_get_logger:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance
        v.return_value = (False, error)
        log_message(mock_message)
        mock_logger_instance.error.assert_called_with(
            log_prefix, message, error)


def test_get_message_data_valid_rating():
    """Test get message data returns correct list."""
    message = '{"at": "2025-05-14T12:33:35.076377+01:00", "site": "5", "val": 3}'
    json_message = {"at": "2025-05-14T12:33:35.076377+01:00",
                    "site": "5", "val": 3}
    log_prefix = "Formatted message as list: %s"
    mock_message = Mock()
    mock_message.value.return_value = message.encode()
    with patch("consumer.is_valid_message") as v, patch("consumer.logging.getLogger") as mock_get_logger:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance
        v.return_value = (True, "")
        actual = get_message_data(mock_message)
        mock_logger_instance.info.assert_called_with(
            log_prefix, json_message)
    assert actual == ["2025-05-14T12:33:35.076377+01:00", "5", 3]


def test_get_message_data_valid():
    """Test get message data returns correct list."""
    message = '{"at": "2025-05-14T12:33:35.076377+01:00", "site": "5", "val": -1, "type": 0}'
    json_message = {"at": "2025-05-14T12:33:35.076377+01:00",
                    "site": "5", "val": -1, "type": 0}
    log_prefix = "Formatted message as list: %s"
    mock_message = Mock()
    mock_message.value.return_value = message.encode()
    with patch("consumer.is_valid_message") as v, patch("consumer.logging.getLogger") as mock_get_logger:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance
        v.return_value = (True, "")
        actual = get_message_data(mock_message)
        mock_logger_instance.info.assert_called_with(
            log_prefix, json_message)
    assert actual == ["2025-05-14T12:33:35.076377+01:00", "5", -1, 0]


@mark.parametrize("test_input, expected", [({"at": "2025-05-14T12:33:35.076377+01:00",
                                             "site": "5", "val": -1, "type": 0}, (True, "Valid message.")),
                                           ({"at": "2025-05-14T12:33:35.076377+01:00",
                                               "site": "5", "val": 4}, (True, "Valid message.")),
                                           ({"at": "2025-05-14T12:33:35.076377+01:00",
                                             "site": "5"}, (False, "No key called 'val'"))])
def test_is_valid_message(test_input, expected):
    """Test if valid message returns expected bool."""
    actual = is_valid_message(test_input)
    assert actual == expected
