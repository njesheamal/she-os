"""create field notes

Revision ID: 8c2d4e5f6a7b
Revises: 7ed26197f8a6
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "8c2d4e5f6a7b"
down_revision: Union[str, Sequence[str], None] = "7ed26197f8a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "field_notes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("theme", sa.String(length=255), nullable=True),
        sa.Column("poem", sa.Text(), nullable=False),
        sa.Column("media", JSONB(), nullable=True),
        sa.Column("essay", sa.Text(), nullable=True),
        sa.Column("excerpt", sa.String(length=500), nullable=True),
        sa.Column("initiative_id", sa.Uuid(), nullable=True),
        sa.Column(
            "published_at", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("title <> ''", name=op.f("ck_field_notes_title_not_empty")),
        sa.CheckConstraint("poem <> ''", name=op.f("ck_field_notes_poem_not_empty")),
        sa.CheckConstraint(
            "status IN ('draft', 'published')",
            name=op.f("ck_field_notes_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["initiative_id"],
            ["initiatives.id"],
            name=op.f("fk_field_notes_initiative_id_initiatives"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_field_notes")),
    )
    op.create_index(
        op.f("ix_field_notes_slug"), "field_notes", ["slug"], unique=True
    )
    op.create_index(
        op.f("ix_field_notes_status"), "field_notes", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_field_notes_initiative_id"),
        "field_notes",
        ["initiative_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_field_notes_published_at"),
        "field_notes",
        ["published_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("field_notes")