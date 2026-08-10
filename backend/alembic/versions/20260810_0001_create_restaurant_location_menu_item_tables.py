"""create restaurant location menu item tables

Revision ID: 20260810_0001
Revises:
Create Date: 2026-08-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260810_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("website_url", sa.String(length=2048), nullable=True),
        sa.Column("source_url", sa.String(length=2048), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_restaurants_name", "restaurants", ["name"])

    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_locations_restaurant_id", "locations", ["restaurant_id"])

    op.create_table(
        "menu_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("price", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column("protein_grams", sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column("calories", sa.Integer(), nullable=True),
        sa.Column("source_url", sa.String(length=2048), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_menu_items_category", "menu_items", ["category"])
    op.create_index("ix_menu_items_name", "menu_items", ["name"])
    op.create_index("ix_menu_items_price", "menu_items", ["price"])
    op.create_index("ix_menu_items_restaurant_id", "menu_items", ["restaurant_id"])


def downgrade() -> None:
    op.drop_index("ix_menu_items_restaurant_id", table_name="menu_items")
    op.drop_index("ix_menu_items_price", table_name="menu_items")
    op.drop_index("ix_menu_items_name", table_name="menu_items")
    op.drop_index("ix_menu_items_category", table_name="menu_items")
    op.drop_table("menu_items")
    op.drop_index("ix_locations_restaurant_id", table_name="locations")
    op.drop_table("locations")
    op.drop_index("ix_restaurants_name", table_name="restaurants")
    op.drop_table("restaurants")
