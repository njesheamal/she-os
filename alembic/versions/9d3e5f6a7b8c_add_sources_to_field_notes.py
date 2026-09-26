"""add sources to field notes

Revision ID: 9d3e5f6a7b8c
Revises: 8c2d4e5f6a7b
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import JSONB
import sqlalchemy as sa


revision: str = "9d3e5f6a7b8c"
down_revision: Union[str, Sequence[str], None] = "8c2d4e5f6a7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "field_notes", sa.Column("sources", JSONB(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("field_notes", "sources")