from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_product_service, get_request_user_id
from app.exceptions import (
    ProductAlreadyExistsException,
    ProductNotFoundException,
    PermissionDeniedException,
)
from app.product.schemas import ProductSchema, CreateProductSchema, UpdtaeProductSchema
from app.product.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get(path="/bestsellers", response_model=List[ProductSchema])
async def read_bestsellers(
    bestsellers_service: Annotated[ProductService, Depends(get_product_service)]
):
    return await bestsellers_service.get_bestsellers()


@router.get(path="/all", response_model=List[ProductSchema])
async def read_products(
    product_service: Annotated[ProductService, Depends(get_product_service)]
):
    return await product_service.read_products()


@router.get(path="/{product_id}", response_model=ProductSchema)
async def read_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        new_product: ProductSchema = await product_service.read_product(product_id)
        return new_product
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post(path="/", response_model=ProductSchema)
async def create_product(
    body: CreateProductSchema,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
):
    try:
        return await product_service.create_product(body=body, user_id=user_id)
    except ProductAlreadyExistsException as e:
        raise HTTPException(status_code=403, detail=e.detail)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.patch(path="/{product_id}", response_model=UpdtaeProductSchema)
async def update_product_name(
    product_id: int,
    product_name: str,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
):
    try:
        return await product_service.update_product_name(
            product_id=product_id, product_name=product_name, user_id=user_id
        )

    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.delete(path="/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    product_service: Annotated[ProductService, Depends(get_product_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
):
    try:
        return await product_service.delete_product(
            product_id=product_id, user_id=user_id
        )

    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
