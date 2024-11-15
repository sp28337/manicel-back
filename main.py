from fastapi import FastAPI

from handlers import routers


app = FastAPI(title="MANICEL")


for router in routers:
    app.include_router(router)
