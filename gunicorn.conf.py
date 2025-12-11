import os

# Конфигурация Gunicorn
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", 1))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5

# Логирование
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(D)s"'
error_logfile = "-"  # Логи в stderr (journalctl будет их ловить)
access_logfile = "-"  # Логи в stdout

# Graceful shutdown
graceful_timeout = 30
