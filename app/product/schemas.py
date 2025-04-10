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


class BestsellerSchema(DefaultSchema):
    id: int
    ingredients: list
    flavor: FlavorSchema | None


class ProductSchema(DefaultSchema):
    id: int
    category: CategorySchema
    flavor: FlavorSchema | None
    reviews: int | None
    attention: str | None
    features: str | None
    result: str | None


class CreateProductSchema(DefaultSchema):
    category_id: int
    flavor_id: int


class UpdtaeProductSchema(DefaultSchema):
    id: int
