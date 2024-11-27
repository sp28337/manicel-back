from pydantic import BaseModel, ConfigDict


class DefaultSchema(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class IngredientSchema(DefaultSchema):
    pass


class CategorySchema(DefaultSchema):
    pass


class FlavorSchema(DefaultSchema):
    ingredients: list[IngredientSchema]


class ProductSchema(DefaultSchema):
    id: int
    category: CategorySchema
    flavor: FlavorSchema | None


class CreateProductSchema(DefaultSchema):
    category_id: int
    flavor_id: int


class UpdtaeProductSchema(DefaultSchema):
    id: int
