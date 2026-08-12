from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import InboundShipmentStatus


class InboundShipment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "inbound_shipments"

    inbound_shipment_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    tracking_number: Mapped[str | None] = mapped_column(String(100))
    carrier_name: Mapped[str | None] = mapped_column(String(100))
    destination_inventory_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("inventory_locations.id"), index=True
    )
    shipped_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )
    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), index=True
    )
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("inbound_shipment_number <> ''", name="number_not_empty"),
        CheckConstraint(status_in(InboundShipmentStatus), name="status_valid"),
        CheckConstraint("received_at >= shipped_at", name="dates_ordered"),
    )
