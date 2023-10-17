from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .review import Review
    from .account import Account


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    account: Mapped["Account"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
