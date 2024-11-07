from typing import Optional

from pydantic import BaseModel, Field


class ProductsSchema(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    category_id: int

    class Config:
        from_attributes = True
