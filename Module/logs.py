import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    # Project root directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Logs directory inside project root
    LOG_DIR = os.path.join(BASE_DIR, "Logs")

    # Create Logs folder if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Absolute paths for log files
    system_log_path = os.path.join(LOG_DIR, "system.log")
    error_log_path = os.path.join(LOG_DIR, "error.log")

    # SYSTEM LOG handler (INFO and above)
    system_handler = RotatingFileHandler(
        system_log_path,
        maxBytes=2 * 1024 * 1024,  # 2 MB
        backupCount=3,
        encoding="utf-8"
    )
    system_handler.setLevel(logging.INFO)
    system_handler.setFormatter(formatter)

    # ERROR LOG handler (only ERROR and CRITICAL)
    error_handler = RotatingFileHandler(
        error_log_path,
        maxBytes=2 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # ROOT LOGGER
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if already added
    if not logger.handlers:
        logger.addHandler(system_handler)
        logger.addHandler(error_handler)

    return logger


# Example usage
if __name__ == "__main__":
    logger = setup_logger()

    logger.exception("heheh")