from datetime import date
from uuid import UUID

from sqlalchemy import (
    CHAR, 
    CheckConstraint, 
    Date, 
    ForeignKey, 
    String, 
    Text)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import PurchaseOrderStatus


class PurchaseOrder(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "purchase_orders"

    purchase_order_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    partner_id: Mapped[UUID] = mapped_column(
        ForeignKey("partners.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    expected_date: Mapped[date | None] = mapped_column(Date)
    currency_code: Mapped[str | None] = mapped_column(CHAR(3))
    notes: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(
            "purchase_order_number <> ''", name="number_not_empty"
        ),
        CheckConstraint(status_in(PurchaseOrderStatus), name="status_valid"),
        CheckConstraint("expected_date >= order_date", name="dates_ordered"),
        CheckConstraint(
            "currency_code ~ '^[A-Z]{3}$'", name="currency_code_valid"
        ),
    )
