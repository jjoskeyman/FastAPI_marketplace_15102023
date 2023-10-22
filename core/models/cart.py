from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import ProductRelationMixin


class Cart(ProductRelationMixin, Base):
    _product_back_populates_ = "cart"
    _user_id_unique_ = True

    quantity: Mapped[int] = mapped_column(default=1)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), unique=True, nullable=True
    )
    orders = relationship("Order", back_populates="cart", uselist=False)
    # def __str__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, status={self.status!r}, user_id={self.user_id})"
    #
    # def __repr__(self):
    #     return str(self)
