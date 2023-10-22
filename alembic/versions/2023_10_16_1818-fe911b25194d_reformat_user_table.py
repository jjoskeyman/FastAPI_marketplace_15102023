"""reformat user table

Revision ID: fe911b25194d
Revises: ad998f93ff5d
Create Date: 2023-10-16 18:18:34.106778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe911b25194d"
down_revision: Union[str, None] = "ad998f93ff5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("username", sa.String(length=32), nullable=False))
    op.drop_constraint("users_email_key", "users", type_="unique")
    op.drop_constraint("users_user_name_key", "users", type_="unique")
    op.create_unique_constraint(None, "users", ["username"])
    op.drop_column("users", "first_name")
    op.drop_column("users", "email")
    op.drop_column("users", "user_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("user_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "users", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "users",
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "users", type_="unique")
    op.create_unique_constraint("users_user_name_key", "users", ["user_name"])
    op.create_unique_constraint("users_email_key", "users", ["email"])
    op.drop_column("users", "username")
    # ### end Alembic commands ###