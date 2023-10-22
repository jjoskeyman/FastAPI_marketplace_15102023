import datetime
from typing import Annotated

from sqlalchemy import text, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    type_annotation_map = {str_256: String(256)}

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
