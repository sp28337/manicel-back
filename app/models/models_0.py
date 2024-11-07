from typing import Optional, List

from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Reccommendations(Base):
    __tablename__ = "reccommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    detail: Mapped[str] = mapped_column(unique=True)


class Descriptions(Base):

    __tablename__ = "descriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    detail: Mapped[str] = mapped_column(unique=True)


class Ingredients(Base):

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    images: Mapped[Optional[str]]
    description: Mapped[Optional[str]]


class Aromas(Base):
    __tablename__ = "aromas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]


class Images(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]


class Warnings(Base):
    __tablename__ = "warnings"

    id: Mapped[int] = mapped_column(primary_key=True)
    detail: Mapped[str] = mapped_column(unique=True)


class Effects(Base):
    __tablename__ = "effects"

    id: Mapped[int] = mapped_column(primary_key=True)
    detail: Mapped[str] = mapped_column(unique=True)


class Countries(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Brands(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Prices(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    size = mapped_column(Numeric(10, 2), unique=True)


class Items(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    price_id: Mapped[int] = mapped_column(ForeignKey("prices.id"))
    aroma_id: Mapped[Optional[int]] = mapped_column(ForeignKey("aromas.id"))
    effect_id: Mapped[Optional[int]] = mapped_column(ForeignKey("effects.id"))
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey("images.id"))
    ingredient_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ingredients.id"))
    reccommendation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reccommendations.id"))
    warning_id: Mapped[Optional[int]] = mapped_column(ForeignKey("warnings.id"))
    description_id: Mapped[Optional[int]] = mapped_column(ForeignKey("descriptions.id"))

