import logging

from .consts import (
    DEFAULT_LOG_FILE,
    AUDIT_LOG_FILE,
    ERROR_LOG_FILE,
    ACCESS_LOG_FILE,
)


def get_log_config():
    return {
        "version": 1,
        "formatters": {
            "default_handler": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default_handler",
            },
            "default_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": DEFAULT_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "default_handler",
            },
            "error_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": ERROR_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "default_handler",
            },
            "access_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": ACCESS_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "default_handler",
            },
            "audit_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": AUDIT_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "default_handler",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console_handler"]},
        "loggers": {
            "werkzeug": {
                "handlers": ["access_handler"],
                "level": "INFO",
                "propagate": False,
            },
            "default": {
                "handlers": ["default_handler"],
                "level": "INFO",
            },
            "error": {
                "handlers": ["error_handler"],
                "level": "ERROR",
            },
            "access": {
                "handlers": ["access_handler"],
                "level": "INFO",
            },
            "audit": {
                "handlers": ["audit_handler"],
                "level": "INFO",
            },
        },
    }


def default_logger():
    return logging.getLogger("default")


def error_logger():
    return logging.getLogger("error")


def access_logger():
    return logging.getLogger("access")


def audit_logger():
    return logging.getLogger("audit")
