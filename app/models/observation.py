from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Observation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "observations"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    observed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )

    __table_args__ = (
        CheckConstraint("title <> ''", name="title_not_empty"),
        CheckConstraint("details <> ''", name="details_not_empty"),
    )
