from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class InboundShipmentLine(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "inbound_shipment_lines"

    inbound_shipment_id: Mapped[UUID] = mapped_column(
        ForeignKey("inbound_shipments.id"), nullable=False, index=True
    )
    purchase_order_line_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_order_lines.id"), nullable=False, index=True
    )
    quantity_shipped: Mapped[Decimal] = mapped_column(
        Numeric(14, 4), nullable=False
    )
    quantity_received: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))
    quantity_accepted: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))
    quantity_damaged: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))
    unit_of_measure_id: Mapped[UUID] = mapped_column(
        ForeignKey("units_of_measure.id"), nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint(
            "inbound_shipment_id",
            "purchase_order_line_id",
            name="shipment_po_line_unique",
        ),
        CheckConstraint("quantity_shipped >= 0", name="quantity_shipped_non_negative"),
        CheckConstraint("quantity_received >= 0", name="quantity_received_non_negative"),
        CheckConstraint("quantity_accepted >= 0", name="quantity_accepted_non_negative"),
        CheckConstraint("quantity_damaged >= 0", name="quantity_damaged_non_negative"),
    )
