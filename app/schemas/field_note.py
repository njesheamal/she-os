from datetime import datetime
import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.common import SLUG_PATTERN
from app.enums import FieldNoteStatus, MediaKind, SourceKind

class MediaRef(BaseModel):
    url: str = Field(min_length=1)
    kind: MediaKind
    alt: str | None = None
    caption: str | None = None


class SourceRef(BaseModel):
    label: str = Field(min_length=1)
    url: str | None = None
    kind: SourceKind | None = None


class FieldNoteBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255, pattern=SLUG_PATTERN)
    theme: str | None = None
    poem: str = Field(min_length=1)
    media: list[MediaRef] | None = None
    essay: str | None = None
    sources: list[SourceRef] | None = None
    excerpt: str | None = Field(default=None, max_length=500)
    tags: list[str] | None = Field(default=None)

class FieldNoteCreate(FieldNoteBase):
    """Always created as a draft."""


class FieldNoteUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(
        default=None, min_length=1, max_length=255, pattern=SLUG_PATTERN
    )
    theme: str | None = None
    poem: str | None = Field(default=None, min_length=1)
    media: list[MediaRef] | None = None
    essay: str | None = None
    sources: list[SourceRef] | None = None
    excerpt: str | None = Field(default=None, max_length=500)
    tags: list[str] | None = Field(default=None)

class FieldNoteRead(FieldNoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: FieldNoteStatus
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime