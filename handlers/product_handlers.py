from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_product_service, get_request_user_id, get_request_admin
from exceptions import ProductAlreadyExistsException, ProductNotFoundException
from schemas import ProductSchema, CreateProductSchema, UpdtaeProductSchema
from services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get(path="/all", response_model=List[ProductSchema])
async def read_products(
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return product_service.read_products()


@router.get(path="/{product_id}", response_model=ProductSchema)
async def read_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    try:
        new_product: ProductSchema = product_service.read_product(product_id)
        return new_product
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )


@router.post(path="/", response_model=ProductSchema)
async def create_product(
    body: CreateProductSchema,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    is_admin: Annotated[bool, Depends(get_request_admin)]
    # user_id: Annotated[int, Depends(get_request_user_id)]
):
    try:
        return product_service.create_product(body)
    except ProductAlreadyExistsException as e:
        raise HTTPException(
            status_code=403,
            detail=e.detail
        )


@router.patch(path="/{product_id}", response_model=UpdtaeProductSchema)
async def update_product_name(
    product_id: int,
    product_name: str,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    # user_id: Annotated[int, Depends(get_request_user_id)],
    is_admin: Annotated[bool, Depends(get_request_admin)]
):
    try:
        return product_service.update_product_name(product_id, product_name)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )


@router.delete(path="/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    is_admin: Annotated[bool, Depends(get_request_admin)]
    # user_id: Annotated[int, Depends(get_request_user_id)]
):
    try:
        return product_service.delete_product(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
