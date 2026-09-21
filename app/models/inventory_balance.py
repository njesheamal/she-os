from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class InventoryBalance(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "inventory_balances"

    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("items.id"), nullable=False, index=True
    )
    inventory_location_id: Mapped[UUID] = mapped_column(
        ForeignKey("inventory_locations.id"), nullable=False, index=True
    )
    quantity_on_hand: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    unit_of_measure_id: Mapped[UUID] = mapped_column(
        ForeignKey("units_of_measure.id"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "item_id", "inventory_location_id", name="item_location_unique"
        ),
        CheckConstraint("quantity_on_hand >= 0", name="quantity_on_hand_non_negative"),
    )
