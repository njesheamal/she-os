from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import DecisionStatus


class Decision(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "decisions"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    decision_summary: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    decided_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )

    __table_args__ = (
        CheckConstraint("title <> ''", name="title_not_empty"),
        CheckConstraint("decision_summary <> ''", name="summary_not_empty"),
        CheckConstraint(status_in(DecisionStatus), name="status_valid"),
    )
