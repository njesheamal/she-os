from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import ItemStatus

SLUG_PATTERN = r"^[a-z0-9]+(_[a-z0-9]+)*$"


class ItemBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    name: str = Field(
        min_length=1, 
        max_length=255,
        examples=["Mutinta Licorice 10in"]
    )
    slug: str = Field(
        min_length=1, 
        max_length=255, 
        pattern=SLUG_PATTERN,
        examples=["mutinta_10in_licorice"]
    )
    sku: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100,
        examples=["SUMA-MUT-10-LIC"]
    )
    item_type_id: UUID
    description: str | None = None
    status: ItemStatus


class ItemCreate(ItemBase):
    """What a client sends to create an item."""


class ItemUpdate(BaseModel):
    """What a client sends to modify an item. All fields optional."""

    name: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=255,
        examples=["Mutinta Licorice 10in"]
    )
    slug: str | None = Field(
        default=None, min_length=1, 
        max_length=255, 
        pattern=SLUG_PATTERN,
        examples=["mutinta_10in_licorice"]
    )
    sku: str | None = Field(
        default=None, 
        min_length=1, 
        max_length=100,
        examples=["SUMA-MUT-10-LIC"]
    )
    item_type_id: UUID | None = None
    description: str | None = None
    status: ItemStatus | None = None


class ItemRead(ItemBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
