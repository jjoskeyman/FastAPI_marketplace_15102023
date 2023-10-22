from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User
    from .product import Product


class UserRelationMixin:
    _user_id_nullable_: bool = False
    _user_id_unique_: bool = False
    _user_back_populates_: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            unique=cls._user_id_unique_,
            nullable=cls._user_id_nullable_,
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=cls._user_back_populates_,
        )


class ProductRelationMixin:
    _product_id_nullable_: bool = False
    _product_id_unique_: bool = False
    _product_back_populates_: str | None = None

    @declared_attr
    def product_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("products.id"),
            unique=cls._product_id_unique_,
            nullable=cls._product_id_nullable_,
        )

    @declared_attr
    def product(cls) -> Mapped["Product"]:
        return relationship(
            "Product",
            back_populates=cls._product_back_populates_,
        )
