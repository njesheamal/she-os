"""add publishing initiative type

Revision ID: 71605574e09c
Revises: 44f1b3c7682e
Create Date: 2026-08-27 22:34:18.408893

"""
from typing import Sequence, Union
from uuid import UUID

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71605574e09c'
down_revision: Union[str, Sequence[str], None] = '44f1b3c7682e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PUBLISHING_ID = UUID("33333333-0000-4000-8000-000000000004")

def _table() -> sa.Table:
    return sa.table(
        "initiative_types",
        sa.column("id", sa.Uuid),
        sa.column("name", sa.String),
        sa.column("slug", sa.String),
    )

def upgrade() -> None:
    op.bulk_insert(
        _table(),
        [{"id": PUBLISHING_ID, "name": "publishing", "slug": "publishing"}],
    )


def downgrade() -> None:
    tbl = _table()
    op.execute(tbl.delete().where(tbl.c.id == PUBLISHING_ID))