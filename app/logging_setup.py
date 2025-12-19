import logging
import sys
from logging.config import dictConfig

from app.settings import get_settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log.update(record.extra)

        return __import__("json").dumps(log, ensure_ascii=False)


def setup_logging() -> None:
    settings = get_settings()
    is_prod = settings.ENV == "prod"

    handlers = {
        "default": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json" if is_prod else "default",
        }
    }

    formatters = {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        },
        "json": {
            "()": JsonFormatter,
        },
    }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": formatters,
            "handlers": handlers,
            "root": {
                "level": "INFO" if is_prod else "DEBUG",
                "handlers": ["default"],
            },
            "loggers": {
                "uvicorn.access": {"level": "WARNING"},
                "uvicorn.error": {"level": "INFO"},
                "gunicorn.error": {"level": "INFO"},
                "gunicorn.access": {"level": "WARNING"},
                "asyncio": {"level": "WARNING"},
            },
        }
    )

    logging.getLogger(__name__).info(
        "Logging initialized",
        extra={"extra": {"env": settings.ENV}},
    )
