from pydantic import BaseModel, ConfigDict


class SearchSchema(BaseModel):
    id: int
    name: str
    name_ru: str | None
    type: str
    articule: int

    model_config = ConfigDict(from_attributes=True)
