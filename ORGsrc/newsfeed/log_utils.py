import sys

import loguru

DEFAULT_FORMAT = (
    "<level>[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [{file} | {function} | line {line}]</> {message}"
)


def configure_logger(log_level: str = "INFO", format: str = DEFAULT_FORMAT) -> "loguru.Logger":
    logger = loguru.logger
    logger.remove()
    logger.add(
        sys.stdout,
        format=format,
        level=log_level,
        colorize=True,
    )
    return logger
