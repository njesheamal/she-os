from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from decimal import Decimal


class InventoryMovement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "inventory_movements"

    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("items.id"), nullable=False, index=True
    )
    inventory_location_id: Mapped[UUID] = mapped_column(
        ForeignKey("inventory_locations.id"), nullable=False, index=True
    )
    inventory_movement_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("inventory_movement_types.id"), nullable=False, index=True
    )
    inbound_shipment_line_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("inbound_shipment_lines.id")
    )
    related_movement_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("inventory_movements.id")
    )
    quantity_delta: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    unit_of_measure_id: Mapped[UUID] = mapped_column(
        ForeignKey("units_of_measure.id"), nullable=False
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("quantity_delta <> 0", name="quantity_delta_non_zero"),
    )
