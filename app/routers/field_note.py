from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.enums import FieldNoteStatus
from app.schemas.field_note import (
    FieldNoteCreate,
    FieldNoteRead,
    FieldNoteUpdate,
)
from app.services import field_note as field_note_service
from app.services.field_note import (
    FieldNoteNotFoundError,
    FieldNoteSlugConflictError,
    FieldNoteInvalidTagError,
)

router = APIRouter(prefix="/field-notes", tags=["field-notes"])


@router.get("", response_model=list[FieldNoteRead])
def list_field_notes(
    status_filter: FieldNoteStatus | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return field_note_service.list_field_notes(
        db, status=status_filter, limit=limit, offset=offset
    )


@router.post("", response_model=FieldNoteRead, status_code=status.HTTP_201_CREATED)
def create_field_note(payload: FieldNoteCreate, db: Session = Depends(get_db)):
    try:
        return field_note_service.create_field_note(db, payload)
    except FieldNoteSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except FieldNoteInvalidTagError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.get("/{field_note_id}", response_model=FieldNoteRead)
def get_field_note(field_note_id: UUID, db: Session = Depends(get_db)):
    try:
        return field_note_service.get_field_note(db, field_note_id)
    except FieldNoteNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.patch("/{field_note_id}", response_model=FieldNoteRead)
def update_field_note(
    field_note_id: UUID,
    payload: FieldNoteUpdate,
    db: Session = Depends(get_db),
):
    try:
        return field_note_service.update_field_note(db, field_note_id, payload)
    except FieldNoteNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except FieldNoteSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except FieldNoteInvalidTagError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.post("/{field_note_id}/publish", response_model=FieldNoteRead)
def publish_field_note(field_note_id: UUID, db: Session = Depends(get_db)):
    try:
        return field_note_service.publish_field_note(db, field_note_id)
    except FieldNoteNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.delete("/{field_note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_field_note(field_note_id: UUID, db: Session = Depends(get_db)):
    try:
        field_note_service.delete_field_note(db, field_note_id)
    except FieldNoteNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc