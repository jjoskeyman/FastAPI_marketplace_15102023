import enum
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .cart import Cart


class OrderStatus(enum.Enum):
    accepted = "Accepted"
    sent = "Sent"
    received = "Received"


class Order(UserRelationMixin, Base):
    _user_back_populates_ = "orders"

    status: Mapped[str] = mapped_column(default=OrderStatus.accepted)
    # status: Mapped[OrderStatus]
    comment: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    # cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), unique=True)
    # cart = relationship("Cart", back_populates="orders")
    # def __str__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, status={self.status!r}, user_id={self.user_id})"
    #
    # def __repr__(self):
    #     return str(self)
