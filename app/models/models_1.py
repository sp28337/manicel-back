from typing import Optional, Annotated
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class FlavorTypes(str, Enum):
    mango = "манго"
    babl_gam = "babl_gam"
    mintole = "mintole"
    citrus = "citrus"
    ingir = "ingir"
    cocos = "cocos"
    caramel = "cereals"
    persik = "persik"
    malina = "malina"
    apple = "apple"
    lavanda = "lavanda"




class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]


class Flavors(Base):
    __tablename__ = "flavors"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]


class Ingredients(Base):
    __tablename__ = "ingredients"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]


class Products(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    flavor_id: Mapped[Optional[str]] = mapped_column(ForeignKey("flavors.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))


# class ProductFlavors(Base):
#     __tablename__ = "product_flavors"
#
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
#     flavor_id: Mapped[int] = mapped_column(ForeignKey("flavors.id"), primary_key=True)


class FlavorIngredients(Base):
    __tablename__ = "flavor_ingredients"

    flavor_id: Mapped[int] = mapped_column(ForeignKey("flavors.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)
