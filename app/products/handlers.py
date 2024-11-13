from typing import Annotated
from fastapi import APIRouter, Depends

from app.depends import get_product_service
from app.products.schema import ProductsSchema, ProductSchema
from app.products.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get(path="/all", response_model=list[ProductsSchema])
async def read_products(
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.read_products()


@router.get(path="/{product_name}", response_model=ProductSchema)
async def read_product(
        product_name: str,
        product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.read_product(product_name)
