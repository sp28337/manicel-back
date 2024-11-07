from typing import Annotated
from fastapi import APIRouter, Depends

from app.depends import get_product_service
from app.products.schema import ProductsSchema
from app.products.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get(path="/all", response_model=list[ProductsSchema])
async def read_products(
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.get_products()


@router.get(path="/{product_id}", response_model=ProductsSchema)
async def read_product(product_id: int, product_service: Annotated[ProductService, Depends(get_product_service)]):
    return product_service.get_product(product_id)
