import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, str_256


class ProductCategory(enum.Enum):
    electronics = "electronics"
    furniture = "furniture"
    phones = "phones"


class Product(Base):
    product_name: Mapped[str]
    description: Mapped[str_256 | None]
    price: Mapped[int]
    product_category: Mapped[str | None]
    # product_category: Mapped[ProductCategory]
    # review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=True)
