from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import PartnerStatus


class Partner(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "partners"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    partner_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("partner_types.id"), nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    website: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))

    __table_args__ = (
        CheckConstraint("name <> ''", name="name_not_empty"),
        CheckConstraint("slug <> ''", name="slug_not_empty"),
        CheckConstraint(status_in(PartnerStatus), name="status_valid"),
    )
