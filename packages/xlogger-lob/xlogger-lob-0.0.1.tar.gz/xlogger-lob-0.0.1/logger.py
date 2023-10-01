import loguru
import sys

logger = loguru.logger


def setup_logger(log_path="logs/bcp_parser"):
    config = {
        "handlers": [
            {
                "sink": log_path + "_{time:YYYY-MM-DD}.log",
                "rotation": "5 MB",
                "retention": "3 days",
                "format": "{time:YYYY-MM-DD HH:mm:ss} - {level} - {file}:{line} - {message}",
                "level": "INFO",
            },
            {
                "sink": sys.stdout,  # <-- Change here
                "level": "INFO",
            },
        ]
    }

    logger.configure(**config)
