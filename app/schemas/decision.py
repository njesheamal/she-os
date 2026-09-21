from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import DecisionStatus


class DecisionBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    title: str = Field(min_length=1, max_length=255)
    decision_summary: str = Field(min_length=1)
    reasoning: str | None = None
    status: DecisionStatus
    decided_at: datetime | None = None


class DecisionCreate(DecisionBase):
    """What a client sends to create a decision."""


class DecisionUpdate(BaseModel):
    """What a client sends to modify a decision. All fields optional."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    decision_summary: str | None = Field(default=None, min_length=1)
    reasoning: str | None = None
    status: DecisionStatus | None = None
    decided_at: datetime | None = None


class DecisionRead(DecisionBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
