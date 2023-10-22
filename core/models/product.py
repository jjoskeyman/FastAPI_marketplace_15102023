import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_256

if TYPE_CHECKING:
    # from .cart import Cart
    from .order import Order
    from .order_product_association import OrderProductAssociation


class ProductCategory(enum.Enum):
    electronics = "electronics"
    furniture = "furniture"
    phones = "phones"

###cChhheee
class Product(Base):
    product_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str_256 | None]
    price: Mapped[int] = mapped_column(default=100)
    product_category: Mapped[str | None]
    # product_category: Mapped[ProductCategory]
    # review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=True)
    # cart: Mapped["Cart"] = relationship(back_populates="product")
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products",
    # )
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
