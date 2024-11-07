from fastapi import FastAPI

from app.products.handlers import router as items_router

app = FastAPI(title="MANICEL")


app.include_router(items_router)

