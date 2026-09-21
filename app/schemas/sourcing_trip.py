from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import SourcingTripStatus
from app.common import SLUG_PATTERN


class SourcingTripBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["OrientalSpring'26"]
    )
    slug: str = Field(
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["oriental_spring_26"]
    )
    description: str | None = None
    status: SourcingTripStatus
    start_date: date | None = Field(
        default=None,
        examples=["2026-03-01"]
    )
    end_date: date | None = Field(
        default=None,
        examples=["2026-03-21"]
    )


class SourcingTripCreate(SourcingTripBase):
    """What a client sends to create a sourcing trip."""


class SourcingTripUpdate(BaseModel):
    """What a client sends to modify a sourcing trip. All fields optional."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["OrientalSpring'26"]
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["oriental_spring_26"]
    )
    description: str | None = None
    status: SourcingTripStatus | None = None
    start_date: date | None = Field(
        default=None,
        examples=["2026-03-01"]
    )
    end_date: date | None = Field(
        default=None,
        examples=["2026-03-21"]
    )


class SourcingTripRead(SourcingTripBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
