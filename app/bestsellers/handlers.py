from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.dependencies import get_bestsellers_service

from app.bestsellers.schemas import (
    BestsellersSchema,
)

from app.bestsellers.service import BestsellersService

router = APIRouter(prefix="/bestsellers", tags=["bestsellers"])


@router.get(path="/bestsellers", response_model=List[BestsellersSchema])
async def get_bestsellers(
    bestsellers_service: Annotated[BestsellersService, Depends(get_bestsellers_service)],
):
    return await bestsellers_service.get_bestsellers()

