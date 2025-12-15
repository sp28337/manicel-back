import logging

from logging.handlers import RotatingFileHandler
from settings import Settings

s = Settings()


def setup_logging():
    """
    Unified logging setup for dev and prod.

    ENV values:
    - ENV=dev  -> console + file, DEBUG
    - ENV=prod -> console only, INFO
    """

    env = s.ENV

    # --- format ---
    log_format = "%(asctime)s " "%(levelname)s " "[%(name)s] " "%(message)s"

    date_format = "%Y-%m-%d %H:%M:%S"

    handlers: list[logging.Handler] = []

    # --- console (always) ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    handlers.append(console_handler)

    # --- file (dev only) ---
    if env == "dev":
        file_handler = RotatingFileHandler(
            "app.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        handlers.append(file_handler)

    # --- root logger ---
    logging.basicConfig(
        level=logging.DEBUG if env == "dev" else logging.INFO,
        handlers=handlers,
        force=True,  # IMPORTANT for gunicorn/uvicorn
    )

    # --- silence noisy libraries ---
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logging.getLogger(__name__).info("Logging initialized (env=%s)", env)
