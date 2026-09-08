"""remove protein fields from the menu contract

Revision ID: 20260907_0003
Revises: 20260907_0002
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260907_0003"
down_revision: Union[str, Sequence[str], None] = "20260907_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("menu_items", "protein_grams")
    op.drop_column("menu_items", "protein_grams_max")


def downgrade() -> None:
    op.add_column("menu_items", sa.Column("protein_grams", sa.Numeric(8, 2), nullable=True))
    op.add_column("menu_items", sa.Column("protein_grams_max", sa.Numeric(8, 2), nullable=True))