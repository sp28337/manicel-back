import logging


from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.product.handlers import router as product_router
from app.user.handlers import router as user_router
from app.user.auth.handlers import router as auth_router

routers = [product_router, user_router, auth_router]


logging.basicConfig(
    # filename="py_log.log",
    level=logging.INFO,
    format=" * [%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    filemode="a"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="MANICEL", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://front:3000", "http://localhost:3000"]
)

for router in routers:
    app.include_router(router)
