from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ObservationBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    title: str = Field(
        min_length=1,
        max_length=255,
        examples=["Silk villages produce raw silk only"]
    )
    details: str = Field(
        min_length=1,
        examples=[
            "Silk villages primarily produce raw silk. Bao Loc manufacturers "
            "are better suited for finished silk sourcing."
        ]
    )
    observed_at: datetime | None = Field(
        default=None,
        examples=["2026-03-12T09:30:00Z"]
    )


class ObservationCreate(ObservationBase):
    """What a client sends to create an observation."""


class ObservationUpdate(BaseModel):
    """What a client sends to modify an observation. All fields optional."""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Silk villages produce raw silk only"]
    )
    details: str | None = Field(
        default=None,
        min_length=1,
        examples=["Bao Loc manufacturers are better suited for finished silk."]
    )
    observed_at: datetime | None = Field(
        default=None,
        examples=["2026-03-12T09:30:00Z"]
    )


class ObservationRead(ObservationBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
