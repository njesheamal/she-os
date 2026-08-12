from uuid import UUID
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PurchaseOrderLine(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "purchase_order_lines"

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"), nullable=False, index=True
    )
    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("items.id"), nullable=False, index=True
    )
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    quantity_ordered: Mapped[Decimal] = mapped_column(
        Numeric(14, 4), nullable=False
    )
    unit_of_measure_id: Mapped[UUID] = mapped_column(
        ForeignKey("units_of_measure.id"), nullable=False
    )
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))

    __table_args__ = (
        UniqueConstraint(
            "purchase_order_id", "line_number", name="po_line_number_unique"
        ),
        CheckConstraint("line_number > 0", name="line_number_positive"),
        CheckConstraint("quantity_ordered >= 0", name="quantity_ordered_non_negative"),
        CheckConstraint("unit_price >= 0", name="unit_price_non_negative"),
    )
