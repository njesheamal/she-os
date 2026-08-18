from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import PartnerStatus


class PartnerBase(BaseModel):
    """Fields a client supplies, shared by create and read."""

    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    partner_type_id: UUID
    description: str | None = None
    status: PartnerStatus
    website: str | None = Field(default=None, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)


class PartnerCreate(PartnerBase):
    """What a client sends to create a partner."""


class PartnerUpdate(BaseModel):
    """What a client sends to modify a partner. All fields optional."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    partner_type_id: UUID | None = None
    description: str | None = None
    status: PartnerStatus | None = None
    website: str | None = Field(default=None, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)


class PartnerRead(PartnerBase):
    """What the API sends back."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
