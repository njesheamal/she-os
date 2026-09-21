from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InventoryMovementCreate(BaseModel):
    """What a client sends to post an inventory movement."""

    item_id: UUID
    inventory_location_id: UUID
    inventory_movement_type_id: UUID
    inbound_shipment_line_id: UUID | None = None
    related_movement_id: UUID | None = None
    quantity_delta: Decimal = Field(
        decimal_places=4,
        examples=["9.0000"]
    )
    unit_of_measure_id: UUID
    occurred_at: datetime = Field(
        examples=["2026-05-21T14:00:00Z"]
    )
    notes: str | None = Field(
        default=None,
        examples=["Received from Naija New Year shipment"]
    )


class InventoryMovementRead(BaseModel):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    item_id: UUID
    inventory_location_id: UUID
    inventory_movement_type_id: UUID
    inbound_shipment_line_id: UUID | None
    related_movement_id: UUID | None
    quantity_delta: Decimal
    unit_of_measure_id: UUID
    occurred_at: datetime
    notes: str | None
    created_at: datetime
    updated_at: datetime
