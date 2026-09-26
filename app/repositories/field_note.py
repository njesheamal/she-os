from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.field_note import FieldNote


def get(db: Session, field_note_id: UUID) -> FieldNote | None:
    return db.get(FieldNote, field_note_id)


def get_by_slug(db: Session, slug: str) -> FieldNote | None:
    return db.scalar(select(FieldNote).where(FieldNote.slug == slug))


def list_all(
    db: Session,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[FieldNote]:
    statement = select(FieldNote)
    if status is not None:
        statement = statement.where(FieldNote.status == status)
    return list(
        db.scalars(
            statement.order_by(FieldNote.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def create(db: Session, field_note: FieldNote) -> FieldNote:
    db.add(field_note)
    db.flush()
    db.refresh(field_note)
    return field_note


def update(db: Session, field_note: FieldNote) -> FieldNote:
    db.add(field_note)
    db.flush()
    db.refresh(field_note)
    return field_note


def delete(db: Session, field_note: FieldNote) -> None:
    db.delete(field_note)
    db.flush()