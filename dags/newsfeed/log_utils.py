import sys

import loguru

DEFAULT_FORMAT = (
    "<level>[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [{file} | {function} | line {line}]</> {message}"
)


def configure_logger(log_level: str = "INFO", format: str = DEFAULT_FORMAT) -> "loguru.Logger":
    """
    Configures the logger with the specified log level and format.

    Args:
        log_level (str, optional): The log level to set for the logger. Defaults to "INFO".
        format (str, optional): The log format to use. Defaults to DEFAULT_FORMAT.

    Returns:
        loguru.Logger: The configured logger instance.
    """
    logger = loguru.logger
    logger.remove()
    logger.add(
        sys.stdout,
        format=format,
        level=log_level,
        colorize=True,
    )
    return logger
