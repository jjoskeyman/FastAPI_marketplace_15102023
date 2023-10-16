from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Product(Base):
    product_name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    price: Mapped[int]
