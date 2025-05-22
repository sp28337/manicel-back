from pydantic import BaseModel, ConfigDict


class BestsellersSchema(BaseModel):
    id: int
    name: str
    name_ru: str | None
    reviews: int | None
    ingredients: list[str]
    type: str

    model_config = ConfigDict(from_attributes=True)
