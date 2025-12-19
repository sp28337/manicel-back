from app.settings import Settings

s = Settings()

bind = s.GUNICORN_BIND
workers = s.GUNICORN_WORKERS
worker_class = "uvicorn.workers.UvicornWorker"

timeout = 120
keepalive = 5
graceful_timeout = 30

accesslog = "-"
errorlog = "-"
loglevel = "info"
