import enum

from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.base import str_256


class ProductBase(BaseModel):
    product_name: str
    description: str
    price: int
    product_category: str
    # review_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    product_name: str | None = None
    description: str | None = None
    price: int | None = None
    product_category: str | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# class ReviewBase(Base):
#     _user_back_populates_ = "reviews"
#
#     title: Mapped[str] = mapped_column(String(100), unique=False)
#     body: Mapped[Text] = mapped_column(
#         Text,
#         default="",
#         server_default="",
#     )
#     rating: Mapped[int | None] = None
#
#     # def __str__(self):
#     #     return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id})"
#     #
#     # def __repr__(self):
#     #     return str(self)
#
#
# class ReviewCreate(ReviewBase):
#     pass
#
#
# class ReviewUpdate(ReviewBase):
#     pass
#
#
# class ReviewUpdatePartial(ReviewCreate):
#     pass
#
#
# class Review(ReviewBase):
#     id: int
