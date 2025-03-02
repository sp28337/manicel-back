from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer import make_amqp_consumer
from app.product.handlers import router as product_router
from app.user.handlers import router as user_router
from app.user.auth.handlers import router as auth_router

routers = [product_router, user_router, auth_router]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_amqp_consumer()
    yield


app = FastAPI(title="MANICEL", lifespan=lifespan)


for router in routers:
    app.include_router(router)


