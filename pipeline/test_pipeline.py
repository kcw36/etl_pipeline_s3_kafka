# pylint:skip-file
"""Tests for pipeline script."""

from pytest import mark
from unittest.mock import Mock, patch, mock_open

from pipeline import (upload_data,
                      input_row)


@mark.parametrize("table, row, expected", [("rating", ["2025-05-14 12:33:35", 1, 2], True),
                                           ("request", [
                                            "2025-05-14 12:33:35", 1, -1, '0.0'], True),
                                           ("request", [
                                            "2025-05-14 12:33:35", 1, -1, '0.0'], False),
                                           ("rating", ["2025-05-14 12:33:35", 1, -1, '0.0'], False)])
def test_input_row_valid(table, row, expected):
    """Test case when input row recieves valid input."""
    with patch("pipeline.is_duplicate") as mock_duplicate, patch("pipeline.get_cursor") as mock_cursor:
        mock_duplicate.return_value = not expected
        mock_cursor.fetchone.return_value = (1)
        mock_conn = Mock()
        actual = input_row(mock_conn, row, table)
    assert actual == expected


@mark.parametrize("data, skip", [([["2025-05-14 12:33:35", 1, 2],
                                   ["2025-05-14 12:33:35", 1, 2],
                                   ["2025-05-14 12:33:35", 1, 2]], True),
                                 ([["2025-05-14 12:33:35", 1, 2],
                                     ["2025-05-14 12:33:35", 1, 2],
                                   ["2025-05-14 12:33:35", 1, 2]], False)])
def test_upload_data_valid(data, skip):
    """Test upload data in the valid case."""
    with patch("pipeline.input_row") as mock_input, patch("pipeline.getLogger") as mock_get_logger, patch("pipeline.Bar") as mock_bar:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance

        mock_input.return_value = not skip

        mock_conn = Mock()

        upload_data(mock_conn, data)
        if skip:
            mock_logger_instance.info.assert_called_with(
                "%s Rows have been skipped.", len(data))
        mock_input.assert_called()
