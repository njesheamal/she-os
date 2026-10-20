"""add tags to field notes

Revision ID: a31694329048
Revises: 9d3e5f6a7b8c
Create Date: 2026-09-26 00:07:27.849156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = "a31694329048"
down_revision: Union[str, Sequence[str], None] = '9d3e5f6a7b8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("field_notes", sa.Column("tags", JSONB(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("field_notes", "tags")