from fastapi import FastAPI

from app.handlers import routers


app = FastAPI(title="MANICEL")


for router in routers:
    app.include_router(router)
