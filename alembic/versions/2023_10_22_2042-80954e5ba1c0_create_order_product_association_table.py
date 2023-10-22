"""create order product association table

Revision ID: 80954e5ba1c0
Revises: 1479c9d697df
Create Date: 2023-10-22 20:42:55.140151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "80954e5ba1c0"
down_revision: Union[str, None] = "1479c9d697df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders",
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("comment", sa.Text(), server_default="", nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "order_product_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )
    op.add_column(
        "accounts", sa.Column("first_name", sa.String(length=40), nullable=True)
    )
    op.add_column(
        "accounts",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "accounts",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column("products", sa.Column("product_category", sa.String(), nullable=True))
    op.add_column(
        "products",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.alter_column("products", "description", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_constraint("products_product_name_key", "products", type_="unique")
    op.add_column(
        "reviews",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "reviews",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.alter_column("reviews", "rating", existing_type=sa.INTEGER(), nullable=True)
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.alter_column("reviews", "rating", existing_type=sa.INTEGER(), nullable=False)
    op.drop_column("reviews", "updated_at")
    op.drop_column("reviews", "created_at")
    op.create_unique_constraint(
        "products_product_name_key", "products", ["product_name"]
    )
    op.alter_column(
        "products", "description", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_column("products", "updated_at")
    op.drop_column("products", "created_at")
    op.drop_column("products", "product_category")
    op.drop_column("accounts", "updated_at")
    op.drop_column("accounts", "created_at")
    op.drop_column("accounts", "first_name")
    op.drop_table("order_product_association")
    op.drop_table("orders")
    # ### end Alembic commands ###
