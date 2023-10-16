from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .review import Review
    from .account import Account


class User(Base):
    user_name: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    account: Mapped["Account"] = relationship(back_populates="user")
