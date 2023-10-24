import enum
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    # from .cart import Cart
    from .product import Product
    from .order_product_association import OrderProductAssociation


class OrderStatus(enum.Enum):
    accepted = "Accepted"
    sent = "Sent"
    received = "Received"


class Order(Base):
    # _user_back_populates_ = "orders"

    status: Mapped[str] = mapped_column(default=OrderStatus.accepted)
    # status: Mapped[OrderStatus]
    comment: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
    # cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), unique=True)
    # cart = relationship("Cart", back_populates="orders")
    # def __str__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, status={self.status!r}, user_id={self.user_id})"
    #
    # def __repr__(self):
    #     return str(self)
