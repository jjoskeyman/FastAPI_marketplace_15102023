from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Account(UserRelationMixin, Base):
    _user_id_unique_ = True
    _user_back_populates_ = "account"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    balance: Mapped[int | None]
    bio: Mapped[str | None]
