from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import InboundShipmentStatus

# ── line schemas ─────────────────────────────────────────────────────

class InboundShipmentLineCreate(BaseModel):
    """What a client sends to add a line to an inbound shipment."""

    purchase_order_line_id: UUID
    quantity_shipped: Decimal = Field(
        gt=0,
        decimal_places=4,
        examples=["10.0000"]
    )
    unit_of_measure_id: UUID
    notes: str | None = Field(
        default=None,
        examples=["Handle with care"]
    )

class InboundShipmentLineUpdate(BaseModel):
    """What a client sends to update a shipment line. All fields optional."""

    quantity_shipped: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=4,
        examples=["1.0000"]
    )
    quantity_received: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=4,
        examples=["1.0000"]
    )
    quantity_accepted: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=4,
        examples=["1.0000"]
    )
    quantity_damaged: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=4,
        examples=["0.0000"]
    )
    unit_of_measure_id: UUID | None = None
    notes: str | None = Field(
        default=None,
        examples=["Slight packaging damage on arrival"]
    )


class InboundShipmentLineRead(BaseModel):
    """A shipment line as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    inbound_shipment_id: UUID
    purchase_order_line_id: UUID
    quantity_shipped: Decimal
    quantity_received: Decimal | None
    quantity_accepted: Decimal | None
    quantity_damaged: Decimal | None
    unit_of_measure_id: UUID
    notes: str | None
    created_at: datetime
    updated_at: datetime


# ── Inbound shipment schemas ──────────────────────────────────────────────────

class InboundShipmentBase(BaseModel):
    """Fields shared by create and read."""

    inbound_shipment_number: str = Field(
        min_length=1,
        max_length=50,
        examples=["SHE-IS-1001"]
    )
    status: InboundShipmentStatus
    tracking_number: str | None = Field(
        default=None,
        max_length=100,
        examples=["1Z999AA10123456784"]
    )
    carrier_name: str | None = Field(
        default=None,
        max_length=100,
        examples=["DHL"]
    )
    destination_inventory_location_id: UUID | None = None
    shipped_at: datetime | None = Field(
        default=None,
        examples=["2026-04-28T10:00:00Z"]
    )
    received_at: datetime | None = Field(
        default=None,
        examples=["2026-05-21T14:00:00Z"]
    )
    notes: str | None = Field(
        default=None,
        examples=["Fragile items — handle with care"]
    )


class InboundShipmentCreate(InboundShipmentBase):
    """What a client sends to create an inbound shipment."""

    model_config = ConfigDict(extra="forbid")

    brand_ids: list[UUID] = Field(
        min_length=1,
        examples=[["1ed4f178-6c86-4444-b501-73ab5cbaa0a9"]]
    )
    lines: list[InboundShipmentLineCreate] = Field(
        default_factory=list,
        examples=[[]]
    )


class InboundShipmentUpdate(BaseModel):
    """What a client sends to modify a shipment. All fields optional."""

    status: InboundShipmentStatus | None = None
    tracking_number: str | None = Field(
        default=None,
        max_length=100,
        examples=["1Z999AA10123456784"]
    )
    carrier_name: str | None = Field(
        default=None,
        max_length=100,
        examples=["DHL"]
    )
    destination_inventory_location_id: UUID | None = None
    shipped_at: datetime | None = Field(
        default=None,
        examples=["2026-04-28T10:00:00Z"]
    )
    received_at: datetime | None = Field(
        default=None,
        examples=["2026-05-21T14:00:00Z"]
    )
    notes: str | None = Field(
        default=None,
        examples=["Updated delivery notes"]
    )


class InboundShipmentRead(InboundShipmentBase):
    """What the API sends back — includes brand associations and lines."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    brand_ids: list[UUID]
    lines: list[InboundShipmentLineRead]
    created_at: datetime
    updated_at: datetime


# ── Latest number schema ──────────────────────────────────────────────────────

class LatestInboundShipmentNumber(BaseModel):
    """Response for the latest-number helper endpoint."""

    latest_inbound_shipment_number: str | None
    suggested_next: str | None
