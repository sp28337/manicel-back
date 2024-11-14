from typing import Optional, List
from pydantic import BaseModel


class IngredientSchema(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class FlavorSchema(BaseModel):
    name: str
    description: Optional[str]
    ingredients: List[IngredientSchema]

    class Config:
        from_attributes = True


class ProductsSchema(BaseModel):
    id: int
    name: str
    category: CategorySchema
    flavor: FlavorSchema | None
    description: str | None = None

    class Config:
        from_attributes = True


class ProductSchema(ProductsSchema):
    description: Optional[str]

    class Config:
        from_attributes = True


class CreateProductSchema(BaseModel):
    name: str
    description: str | None
    category_id: int
    flavor_id: int

    class Config:
        from_attributes = True


class UpdtaeProductSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
