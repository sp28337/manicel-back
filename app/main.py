from fastapi import FastAPI

from app.product.handlers import router as product_router
from app.user.handlers import router as user_router
from app.user.auth.handlers import router as auth_router

routers = [product_router, user_router, auth_router]


app = FastAPI(title="MANICEL")


for router in routers:
    app.include_router(router)
