from datetime import date
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import InitiativeStatus


class Initiative(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "initiatives"

    initiative_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("initiative_types.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    start_date: Mapped[date | None] = mapped_column(Date, index=True)
    end_date: Mapped[date | None] = mapped_column(Date)

    __table_args__ = (
        CheckConstraint("name <> ''", name="name_not_empty"),
        CheckConstraint("slug <> ''", name="slug_not_empty"),
        CheckConstraint(status_in(InitiativeStatus), name="status_valid"),
        CheckConstraint("end_date >= start_date", name="dates_ordered"),
    )
