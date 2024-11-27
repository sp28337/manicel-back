from typing import Optional, Annotated, List

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
unique_name = Annotated[str, mapped_column(unique=True)]


flavor_ingredients = Table(
    "flavor_ingredients",
    Base.metadata,
    Column("flavor_id", ForeignKey("flavors.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True)
)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[unique_name]
    description: Mapped[Optional[str]]

    products: Mapped[List["Product"]] = relationship(
        back_populates="category",
    )


class Flavor(Base):
    __tablename__ = "flavors"

    id: Mapped[intpk]
    name: Mapped[unique_name]
    description: Mapped[Optional[str]]

    ingredients: Mapped[List["Ingredient"]] = relationship(
        secondary="flavor_ingredients",
        back_populates="flavors",
        lazy='joined'
    )

    products: Mapped[List["Product"]] = relationship(
        back_populates="flavor",
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[intpk]
    name: Mapped[unique_name]
    description: Mapped[Optional[str]]

    flavors: Mapped[List["Flavor"]] = relationship(
        secondary="flavor_ingredients",
        back_populates="ingredients",
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[unique_name]
    description: Mapped[Optional[str]]
    flavor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("flavors.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    flavor: Mapped["Flavor"] = relationship(back_populates="products", lazy="joined")
    category: Mapped["Category"] = relationship(back_populates="products", lazy="joined")

# class ProductFlavors(Base):
#     __tablename__ = "product_flavors"
#
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
#     flavor_id: Mapped[int] = mapped_column(ForeignKey("flavors.id"), primary_key=True)


# class FlavorIngredients(Base):
#     __tablename__ = "flavor_ingredients"
#
#     flavor_id: Mapped[int] = mapped_column(ForeignKey("flavors.id"), primary_key=True)
#     ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), primary_key=True)



