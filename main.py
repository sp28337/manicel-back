from fastapi import FastAPI

from handlers.product_handler import router as items_router

app = FastAPI(title="MANICEL")


app.include_router(items_router)

