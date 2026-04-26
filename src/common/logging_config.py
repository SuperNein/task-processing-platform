import logging
import logging.config
from pathlib import Path
from copy import deepcopy


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # до корня проекта
LOG_FILE = BASE_DIR / "app.log"
LOG_FILE_NAME = str(LOG_FILE)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "mode": "a",
            "filename": LOG_FILE_NAME,
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}


def setup_logging(
        level: int | str | None = None,
        log_file: str | None = None,
        use_console: bool = False,
) -> None:
    """
    Setup logging configuration for the application.
    """
    config = deepcopy(LOGGING_CONFIG)

    if level is not None:
        if isinstance(level, int):
            level_name = logging.getLevelName(level)
        else:
            level_name = level.upper()

        if not use_console:
            config["loggers"][""]["handlers"] = ["file"]

        config["handlers"]["console"]["level"] = level_name
        config["handlers"]["file"]["level"] = level_name
        config["loggers"][""]["level"] = level_name

    if log_file is not None:
        config["handlers"]["file"]["filename"] = log_file

    logging.config.dictConfig(config)
