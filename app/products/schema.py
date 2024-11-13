from typing import Optional

from pydantic import BaseModel, Field


class ProductsSchema(BaseModel):
    name: str
    category: str
    flavor: str | None
    ingredients: str
    # description: str | None = None

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    name: str
    category: str
    flavor: str | None
    ingredients: str
    description: Optional[str]

    class Config:
        from_attributes = True
