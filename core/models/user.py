
from sqlalchemy.orm import Mapped
from .base import Base


class User(Base):

    user_name: Mapped[str]
    first_name: Mapped[str]
    email: Mapped[str]
