import re
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common import TAG_PATTERN
from app.enums import FieldNoteStatus
from app.models.field_note import FieldNote
from app.repositories import field_note as field_note_repo
from app.schemas.field_note import FieldNoteCreate, FieldNoteUpdate


class FieldNoteNotFoundError(Exception):
    """No field note exists with the given identifier."""


class FieldNoteSlugConflictError(Exception):
    """A field note with this slug already exists."""

class FieldNoteInvalidTagError(Exception):
    """A tag is empty or not a valid slug-like token"""

def _normalize_tags(value: list[str] | None) -> list[str] | None:
    if value is None:
        return None
    cleaned: list[str] = []
    for raw in value:
        tag = raw.strip().lstrip("#").lower()
        if not tag:
            continue
        if not re.fullmatch(TAG_PATTERN, tag):
            raise FieldNoteInvalidTagError(f"Invalid tag: {raw!r}")
        if tag not in cleaned:
            cleaned.append(tag)
    return cleaned or None

def _raise_conflict(exc: IntegrityError, slug: str | None) -> None:
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""
    if "slug" in constraint:
        raise FieldNoteSlugConflictError(
            f"A field note with slug '{slug}' already exists"
        ) from exc
    raise


def get_field_note(db: Session, field_note_id: UUID) -> FieldNote:
    field_note = field_note_repo.get(db, field_note_id)
    if field_note is None:
        raise FieldNoteNotFoundError(
            f"No field note found with ID {field_note_id}"
        )
    return field_note


def list_field_notes(
    db: Session,
    status: FieldNoteStatus | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[FieldNote]:
    return field_note_repo.list_all(
        db, status=status, limit=limit, offset=offset
    )


def create_field_note(db: Session, payload: FieldNoteCreate) -> FieldNote:
    field_note = FieldNote(
        slug=payload.slug,
        title=payload.title,
        status=FieldNoteStatus.DRAFT,
        tags=_normalize_tags(payload.tags),
        theme=payload.theme,
        poem=payload.poem,
        media=[media.model_dump() for media in payload.media]
        if payload.media
        else None,
        essay=payload.essay,
        sources=[source.model_dump() for source in payload.sources]
        if payload.sources
        else None,
        excerpt=payload.excerpt,
    )
    try:
        field_note = field_note_repo.create(db, field_note)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc, slug=payload.slug)
    db.refresh(field_note)
    return field_note


def update_field_note(
    db: Session, field_note_id: UUID, payload: FieldNoteUpdate
) -> FieldNote:
    field_note = get_field_note(db, field_note_id)
    changes = payload.model_dump(exclude_unset=True)
    if "tags" in changes:
        changes["tags"] = _normalize_tags(changes["tags"])
    for field, value in changes.items():
        setattr(field_note, field, value)
    try:
        field_note = field_note_repo.update(db, field_note)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc, slug=changes.get("slug"))
    db.refresh(field_note)
    return field_note


def publish_field_note(db: Session, field_note_id: UUID) -> FieldNote:
    field_note = get_field_note(db, field_note_id)
    field_note.status = FieldNoteStatus.PUBLISHED
    if field_note.published_at is None:
        field_note.published_at = datetime.now(timezone.utc)
    field_note = field_note_repo.update(db, field_note)
    db.commit()
    db.refresh(field_note)
    return field_note


def delete_field_note(db: Session, field_note_id: UUID) -> None:
    field_note = get_field_note(db, field_note_id)
    field_note_repo.delete(db, field_note)
    db.commit()