from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import PurchaseOrderStatus
from app.common import CURRENCY_CODE_PATTERN


# ── line schemas ──────────────────────────────────────────────────────────────

class PurchaseOrderLineCreate(BaseModel):
    """What a client sends to add a line to a purchase order."""

    item_id: UUID
    description: str | None = Field(
        default=None,
        examples=["Butter Yellow Silk — transaction-specific note"]
    )
    quantity_ordered: Decimal = Field(
        gt=0,
        decimal_places=4,
        examples=[50]
    )
    unit_of_measure_id: UUID
    unit_price: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=4,
        examples=["12.0000"]
    )


class PurchaseOrderLineUpdate(BaseModel):
    """What a client sends to modify a line. All fields optional."""

    description: str | None = Field(
        default=None,
        examples=["Updated note"]
    )
    quantity_ordered: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=4,
        examples=[60]
    )
    unit_of_measure_id: UUID | None = None
    unit_price: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=4,
        examples=["11.5000"]
    )


class PurchaseOrderLineRead(BaseModel):
    """A purchase order line as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    purchase_order_id: UUID
    line_number: int
    item_id: UUID
    description: str | None
    quantity_ordered: Decimal
    unit_of_measure_id: UUID
    unit_price: Decimal | None
    created_at: datetime
    updated_at: datetime


# ── purchase order schemas ────────────────────────────────────────────────────

class PurchaseOrderBase(BaseModel):
    """Fields shared by create and read."""

    purchase_order_number: str = Field(
        min_length=1,
        max_length=50,
        examples=["SHE-PO-1001"]
    )
    partner_id: UUID
    status: PurchaseOrderStatus
    order_date: date = Field(
        examples=["2026-03-14"]
    )
    expected_date: date | None = Field(
        default=None,
        examples=["2026-04-14"]
    )
    currency_code: str | None = Field(
        default=None,
        pattern=CURRENCY_CODE_PATTERN,
        examples=["NGN"]
    )
    production_brief: str | None = Field(
        default=None,
        examples=[
            "Wigs for older women. Focus on shorter styles and colors "
            "older women gravitate toward."
        ]
    )
    notes: str | None = Field(
        default=None,
        examples=["Manager to report selections after one month."]
    )


class PurchaseOrderCreate(PurchaseOrderBase):
    """What a client sends to create a purchase order."""

    model_config = ConfigDict(extra="forbid")

    brand_ids: list[UUID] = Field(
        min_length=1,
        examples=[["1ed4f178-6c86-4444-b501-73ab5cbaa0a9"]]
    )
    lines: list[PurchaseOrderLineCreate] = Field(
        default_factory=list,
        examples=[[]]
    )


class PurchaseOrderUpdate(BaseModel):
    """What a client sends to modify a purchase order. All fields optional."""

    status: PurchaseOrderStatus | None = None
    partner_id: UUID | None = None
    expected_date: date | None = Field(
        default=None,
        examples=["2026-05-01"]
    )
    currency_code: str | None = Field(
        default=None,
        pattern=CURRENCY_CODE_PATTERN,
        examples=["NGN"]
    )
    production_brief: str | None = Field(
        default=None,
        examples=["Focus on shorter styles."]
    )
    notes: str | None = Field(
        default=None,
        examples=["Updated delivery instructions."]
    )


class PurchaseOrderRead(PurchaseOrderBase):
    """What the API sends back — includes brand associations and lines."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    brand_ids: list[UUID]
    lines: list[PurchaseOrderLineRead]
    created_at: datetime
    updated_at: datetime


# ── latest number schema ──────────────────────────────────────────────────────

class LatestPurchaseOrderNumber(BaseModel):
    """Response for the latest-number helper endpoint."""

    latest_purchase_order_number: str | None
    suggested_next: str | None
