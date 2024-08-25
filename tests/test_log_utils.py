import sys
from loguru import logger
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from newsfeed.log_utils import configure_logger, DEFAULT_FORMAT

def test_configure_logger_default():
    with patch.object(logger, 'add') as mock_add, patch.object(logger, 'remove') as mock_remove:
        log_instance = configure_logger()
        
        mock_remove.assert_called_once()
        mock_add.assert_called_once_with(
            sys.stdout,
            format=DEFAULT_FORMAT,
            level="INFO",
            colorize=True,
        )
        
        # Ensure the returned object is the logger instance
        assert log_instance == logger

def test_configure_logger_custom_level():
    custom_level = "DEBUG"
    with patch.object(logger, 'add') as mock_add, patch.object(logger, 'remove') as mock_remove:
        log_instance = configure_logger(log_level=custom_level)
        
        mock_remove.assert_called_once()
        mock_add.assert_called_once_with(
            sys.stdout,
            format=DEFAULT_FORMAT,
            level=custom_level,
            colorize=True,
        )
        
        assert log_instance == logger

def test_configure_logger_custom_format():
    custom_format = "{message} - {level}"
    with patch.object(logger, 'add') as mock_add, patch.object(logger, 'remove') as mock_remove:
        log_instance = configure_logger(format=custom_format)
        
        mock_remove.assert_called_once()
        mock_add.assert_called_once_with(
            sys.stdout,
            format=custom_format,
            level="INFO",
            colorize=True,
        )
        
        assert log_instance == logger

def test_configure_logger_custom_level_and_format():
    custom_level = "WARNING"
    custom_format = "{time} - {message}"
    with patch.object(logger, 'add') as mock_add, patch.object(logger, 'remove') as mock_remove:
        log_instance = configure_logger(log_level=custom_level, format=custom_format)
        
        mock_remove.assert_called_once()
        mock_add.assert_called_once_with(
            sys.stdout,
            format=custom_format,
            level=custom_level,
            colorize=True,
        )
        
        assert log_instance == logger
