from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import InventoryLocationStatus
from app.common import SLUG_PATTERN

COUNTRY_CODE_PATTERN = r"^[A-Z]{2}$"


class InventoryLocationBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    inventory_location_type_id: UUID
    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["Abuja Warehouse"]
    )
    slug: str = Field(
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["abuja_warehouse"]
    )
    description: str | None = None
    status: InventoryLocationStatus
    address_line_1: str | None = Field(
        default=None,
        max_length=255,
        examples=["Taproot Estate, Lugbe"]
    )
    address_line_2: str | None = Field(
        default=None,
        max_length=255,
        examples=["House 4"]
    )
    city: str | None = Field(
        default=None,
        max_length=100,
        examples=["Abuja"]
    )
    region: str | None = Field(
        default=None,
        max_length=100,
        examples=["FCT"]
    )
    postal_code: str | None = Field(
        default=None,
        max_length=20,
        examples=["900001"]
    )
    country_code: str | None = Field(
        default=None,
        pattern=COUNTRY_CODE_PATTERN,
        examples=["NG"]
    )
    active_from: datetime | None = Field(
        default=None,
        examples=["2026-01-06T00:00:00Z"]
    )
    active_until: datetime | None = Field(
        default=None,
        examples=["2027-01-06T00:00:00Z"]
    )


class InventoryLocationCreate(InventoryLocationBase):
    """What a client sends to create an inventory location."""


class InventoryLocationUpdate(BaseModel):
    """What a client sends to modify a location. All fields optional."""

    inventory_location_type_id: UUID | None = None
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Abuja Warehouse"]
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["abuja_warehouse"]
    )
    description: str | None = None
    status: InventoryLocationStatus | None = None
    address_line_1: str | None = Field(
        default=None,
        max_length=255,
        examples=["12 Mpape Road"]
    )
    address_line_2: str | None = Field(
        default=None,
        max_length=255,
        examples=["Unit 4"]
    )
    city: str | None = Field(
        default=None,
        max_length=100,
        examples=["Abuja"]
    )
    region: str | None = Field(
        default=None,
        max_length=100,
        examples=["FCT"]
    )
    postal_code: str | None = Field(
        default=None,
        max_length=20,
        examples=["900001"]
    )
    country_code: str | None = Field(
        default=None,
        pattern=COUNTRY_CODE_PATTERN,
        examples=["NG"]
    )
    active_from: datetime | None = Field(
        default=None,
        examples=["2026-01-06T00:00:00Z"]
    )
    active_until: datetime | None = Field(
        default=None,
        examples=["2027-01-06T00:00:00Z"]
    )


class InventoryLocationRead(InventoryLocationBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
