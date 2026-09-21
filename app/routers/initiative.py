from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.initiative import (
    InitiativeCreate,
    InitiativeRead,
    InitiativeUpdate,
)
from app.services import initiative as initiative_service
from app.services.initiative import (
    InitiativeDateRangeError,
    InitiativeNotFoundError,
    InitiativeSlugConflictError,
    InitiativeTypeNotFoundError,
)

router = APIRouter(prefix="/initiatives", tags=["initiatives"])


@router.get("", response_model=list[InitiativeRead])
def list_initiatives(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return initiative_service.list_initiatives(db, limit=limit, offset=offset)


@router.get("/{initiative_id}", response_model=InitiativeRead)
def get_initiative(initiative_id: UUID, db: Session = Depends(get_db)):
    try:
        return initiative_service.get_initiative(db, initiative_id)
    except InitiativeNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "", response_model=InitiativeRead, status_code=status.HTTP_201_CREATED
)
def create_initiative(
    payload: InitiativeCreate, db: Session = Depends(get_db)
):
    try:
        return initiative_service.create_initiative(db, payload)
    except InitiativeSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (InitiativeTypeNotFoundError, InitiativeDateRangeError) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.patch("/{initiative_id}", response_model=InitiativeRead)
def update_initiative(
    initiative_id: UUID,
    payload: InitiativeUpdate,
    db: Session = Depends(get_db),
):
    try:
        return initiative_service.update_initiative(db, initiative_id, payload)
    except InitiativeNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InitiativeSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (InitiativeTypeNotFoundError, InitiativeDateRangeError) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete("/{initiative_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_initiative(initiative_id: UUID, db: Session = Depends(get_db)):
    try:
        initiative_service.delete_initiative(db, initiative_id)
    except InitiativeNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
