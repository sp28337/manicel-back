import logging

from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.search.handlers import router as search_router
from app.bestsellers.handlers import router as bestsellers_router
from app.product.handlers import router as product_router
from app.user.handlers import router as user_router
from app.user.auth.handlers import router as auth_router
from app.dependencies import get_product_repository
from app.product.repository import ProductRepository
from logging_setup import setup_logging

routers = [product_router, user_router, auth_router, bestsellers_router, search_router]

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="MANICEL")

origins = [
    "http://frontend:3000",
    "http://localhost:3000",
    "https://manicel.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)


@app.get("/app/ping")
async def ping_app():
    return {"text": "app is working"}


@app.get("/db/ping")
async def ping_db(
    task_repository: Annotated[ProductRepository, Depends(get_product_repository)],
):
    await task_repository.ping_db()
