import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.search.handlers import router as search_router
from app.bestsellers.handlers import router as bestsellers_router
from app.user.handlers import router as user_router
from app.user.auth.handlers import router as auth_router
from app.dependencies import get_product_repository
from app.product.handlers import router as product_router
from app.product.repository import ProductRepository
from app.logging_setup import setup_logging
from app.middleware.logging_setup import logging_middleware
from app.settings import get_settings

s = get_settings()
is_prod = s.ENV == "prod"

setup_logging()

logger = logging.getLogger(__name__)

routers = [
    product_router,
    user_router,
    auth_router,
    bestsellers_router,
    search_router,
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="MANICEL",
    lifespan=lifespan,
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json",
)

app.middleware("http")(logging_middleware)

allowed_origins = [
    s.CORS.FRONT_URL,
    s.CORS.DEV_URL,
    s.CORS.PROD_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o for o in allowed_origins if o],
    allow_credentials=True,
    allow_methods=s.CORS.allow_methods,
    allow_headers=s.CORS.allow_headers,
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
