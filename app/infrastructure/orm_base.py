import sqlalchemy
import enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {enum.Enum: sqlalchemy.Enum(enum.Enum, native_enum=False)}
