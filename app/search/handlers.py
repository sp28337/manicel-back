from typing import Annotated, List
from fastapi import APIRouter, Depends

from app.dependencies import get_search_service
from app.search.schemas import SearchSchema
from app.search.service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get(path="/search_products", response_model=List[SearchSchema])
async def get_search_products(
    query: str, search_service: Annotated[SearchService, Depends(get_search_service)]
):
    return await search_service.get_search_products(query)
