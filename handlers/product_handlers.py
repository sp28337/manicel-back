from typing import Annotated, List
from fastapi import APIRouter, Depends

from dependencies import get_product_service
from schemas import ProductsSchema, ProductSchema, CreateProductSchema, UpdtaeProductSchema
from services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get(path="/all", response_model=List[ProductsSchema])
async def read_products(
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.read_products()


@router.get(path="/{product_id}", response_model=ProductSchema)
async def read_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    new_product: ProductSchema = product_service.read_product(product_id)
    return new_product


@router.post(path="/", response_model=ProductSchema)
async def create_product(
    body: CreateProductSchema,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.create_product(body)


@router.patch(path="/{product_id}", response_model=UpdtaeProductSchema)
async def update_product_name(
    product_id: int,
    product_name: str,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.update_product_name(product_id, product_name)


@router.delete(path="/{product_id}")
async def delete_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.delete_product(product_id)
