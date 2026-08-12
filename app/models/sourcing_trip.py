from datetime import date

from sqlalchemy import CheckConstraint, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import SourcingTripStatus


class SourcingTrip(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sourcing_trips"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    start_date: Mapped[date | None] = mapped_column(Date, index=True)
    end_date: Mapped[date | None] = mapped_column(Date)

    __table_args__ = (
        CheckConstraint("name <> ''", name="name_not_empty"),
        CheckConstraint("slug <> ''", name="slug_not_empty"),
        CheckConstraint(status_in(SourcingTripStatus), name="status_valid"),
        CheckConstraint("end_date >= start_date", name="dates_ordered"),
    )
 