from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import FieldNoteStatus


class FieldNote(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "field_notes"

    slug: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    theme: Mapped[str | None] = mapped_column(String(255))
    poem: Mapped[str] = mapped_column(Text, nullable=False)
    media: Mapped[list[dict] | None] = mapped_column(JSONB)
    essay: Mapped[str | None] = mapped_column(Text)
    sources: Mapped[list[dict] | None] = mapped_column(JSONB)
    excerpt: Mapped[str | None] = mapped_column(String(500))
    tags: Mapped[list[str] | None] = mapped_column(JSONB)
    initiative_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("initiatives.id"), index=True
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )

    __table_args__ = (
        CheckConstraint("title <> ''", name="title_not_empty"),
        CheckConstraint("poem <> ''", name="poem_not_empty"),
        CheckConstraint(status_in(FieldNoteStatus), name="status_valid"),
    )