import os

from dotenv import load_dotenv
from uvicorn_worker import UvicornWorker

bind = "0.0.0.0:8000"
workers = 4
worker_class = UvicornWorker

environment = os.getenv("ENVIRONMENT")
print(f"\nEnvironment: {environment}\n")
env = os.path.join(os.getcwd(), f".{environment}.env")
print(f"\nEnv: {env}\n")
if os.path.exists(env):
    load_dotenv(env)

print(os.getenv("YANDEX_CLIENT_ID"))
