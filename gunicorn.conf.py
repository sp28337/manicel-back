import os
from pathlib import Path

from dotenv import load_dotenv

# Устанавливаем рабочую директорию явно
BASE_DIR = Path(__file__).resolve().parent

# Загружаем основной .env файл
env_file = BASE_DIR / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Загружаем специфичный для окружения .env файл
environment = os.getenv("ENVIRONMENT", "local")
specific_env_file = BASE_DIR / f".{environment}.env"
if specific_env_file.exists():
    load_dotenv(specific_env_file, override=True)

# Конфигурация Gunicorn
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", 4))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5

# Логирование
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(D)s"'
error_logfile = "-"  # Логи в stderr (journalctl будет их ловить)
access_logfile = "-"  # Логи в stdout

# Graceful shutdown
graceful_timeout = 30
