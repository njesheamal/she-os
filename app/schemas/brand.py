from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import BrandStatus


class BrandBase(BaseModel):
    """Fields a client supplies, shared by create and update."""

    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: BrandStatus


class BrandCreate(BrandBase):
    """What a client sends to create a brand."""


class BrandUpdate(BaseModel):
    """What a client sends to modify a brand. All fields optional."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: BrandStatus | None = None


class BrandRead(BrandBase):
    """What the API sends back."""

    # by default, pydantic builds objects from dicts, but we want to build them from ORM models, so we set this config option
    # the repo will hand the router a sqlalchemy onject; pydantic needs to read data as attributes
    # from_attributes=True tells pydantic to read data from attributes instead of dict keys
    # in older pudamttoc versions, this was called orm_mode=True
    # see https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
