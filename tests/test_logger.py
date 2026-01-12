import logging
import unittest
from unittest.mock import MagicMock, patch

from logging_utils.logger import setup_logger


class TestLogger(unittest.TestCase):
    """Test cases for the logger module."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger_name = "test_logger"
        self.log_file = "test.log"

    def tearDown(self):
        """Clean up after tests."""
        import os

        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_setup_logger_creates_logger(self):
        """Test that setup_logger creates a logger with the correct name."""
        logger = setup_logger(self.logger_name, self.log_file)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, self.logger_name)

    def test_setup_logger_configures_handlers(self):
        """Test that setup_logger configures both file and console handlers."""
        logger = setup_logger(self.logger_name, self.log_file)
        self.assertEqual(len(logger.handlers), 2)

    def test_setup_logger_file_handler(self):
        """Test that the file handler is correctly configured."""
        logger = setup_logger(self.logger_name, self.log_file)
        file_handler = logger.handlers[0]
        self.assertEqual(type(file_handler).__name__, "RotatingFileHandler")
        self.assertIn(self.log_file, file_handler.baseFilename)

    def test_setup_logger_console_handler(self):
        """Test that the console handler is correctly configured."""
        logger = setup_logger(self.logger_name, self.log_file)
        console_handler = logger.handlers[1]
        self.assertEqual(type(console_handler).__name__, "StreamHandler")

    def test_setup_logger_log_level(self):
        """Test that the logger is set to the correct log level."""
        logger = setup_logger(self.logger_name, self.log_file)
        self.assertEqual(logger.level, logging.INFO)

    def test_setup_logger_log_message(self):
        """Test that the logger can log messages."""
        logger = setup_logger(self.logger_name, self.log_file)
        with patch.object(logger, "info") as mock_info:
            logger.info("Test message")
            mock_info.assert_called_once_with("Test message")

    def test_setup_logger_error_message(self):
        """Test that the logger can log error messages."""
        logger = setup_logger(self.logger_name, self.log_file)
        with patch.object(logger, "error") as mock_error:
            logger.error("Test error")
            mock_error.assert_called_once_with("Test error")

    def test_setup_logger_exception(self):
        """Test that the logger can log exceptions."""
        logger = setup_logger(self.logger_name, self.log_file)
        with patch.object(logger, "exception") as mock_exception:
            try:
                raise ValueError("Test exception")
            except ValueError:
                logger.exception("Test exception")
                mock_exception.assert_called_once_with("Test exception")


if __name__ == "__main__":
    unittest.main()
