from pydantic import BaseModel, ConfigDict


class DefaultSchema(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class IngredientSchema(DefaultSchema):
    pass


class CategorySchema(DefaultSchema):
    pass


class EffectSchema(BaseModel):
    description: str

    model_config = ConfigDict(from_attributes=True)


class VolumeSchema(BaseModel):
    volume: str

    model_config = ConfigDict(from_attributes=True)


class FlavorSchema(DefaultSchema):
    ingredients: list[IngredientSchema]


class BestsellerSchema(BaseModel):
    id: int
    name: str
    name_ru: str | None
    reviews: int | None
    ingredients: list[str]
    type: str

    model_config = ConfigDict(from_attributes=True)


class ExpirationDateSchema(BaseModel):
    before_opening: str | None
    after_opening: str | None

    model_config = ConfigDict(from_attributes=True)


class ComplectationSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(DefaultSchema):
    id: int
    articule: int | None
    name_ru: str | None
    category: CategorySchema
    complectation: ComplectationSchema | None
    flavor: FlavorSchema | None
    reviews: int | None
    attention: str | None
    effects: list[EffectSchema]
    volumes: list[VolumeSchema]
    expiration_date: ExpirationDateSchema | None
    note: str | None


class CategorySchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProductCatalogSchema(BaseModel):
    id: int
    name: str
    name_ru: str | None
    type: str
    articule: int

    model_config = ConfigDict(from_attributes=True)


class CreateProductSchema(DefaultSchema):
    category_id: int
    flavor_id: int


class UpdtaeProductSchema(DefaultSchema):
    id: int
