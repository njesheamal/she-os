from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import InitiativeStatus
from app.common import SLUG_PATTERN


class InitiativeBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    initiative_type_id: UUID
    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["SUMA Packaging"]
    )
    slug: str = Field(
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["suma_packaging"]
    )
    description: str | None = None
    status: InitiativeStatus
    start_date: date | None = Field(
        default=None,
        examples=["2026-01-15"]
    )
    end_date: date | None = Field(
        default=None,
        examples=["2026-06-30"]
    )


class InitiativeCreate(InitiativeBase):
    """What a client sends to create an initiative."""


class InitiativeUpdate(BaseModel):
    """What a client sends to modify an initiative. All fields optional."""

    initiative_type_id: UUID | None = None
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["SUMA Packaging"]
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["suma_packaging"]
    )
    description: str | None = None
    status: InitiativeStatus | None = None
    start_date: date | None = Field(
        default=None,
        examples=["2026-01-15"]
    )
    end_date: date | None = Field(
        default=None,
        examples=["2026-06-30"]
    )


class InitiativeRead(InitiativeBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
