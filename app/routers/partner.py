from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.partner import PartnerCreate, PartnerRead, PartnerUpdate
from app.services import partner as partner_service
from app.services.partner import (
    PartnerNotFoundError,
    PartnerSlugConflictError,
    PartnerTypeNotFoundError,
)

router = APIRouter(prefix="/partners", tags=["partners"])


@router.get("", response_model=list[PartnerRead])
def list_partners(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return partner_service.list_partners(db, limit=limit, offset=offset)


@router.get("/{partner_id}", response_model=PartnerRead)
def get_partner(partner_id: UUID, db: Session = Depends(get_db)):
    try:
        return partner_service.get_partner(db, partner_id)
    except PartnerNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("", response_model=PartnerRead, status_code=status.HTTP_201_CREATED)
def create_partner(payload: PartnerCreate, db: Session = Depends(get_db)):
    try:
        return partner_service.create_partner(db, payload)
    except PartnerSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except PartnerTypeNotFoundError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.patch("/{partner_id}", response_model=PartnerRead)
def update_partner(
    partner_id: UUID,
    payload: PartnerUpdate,
    db: Session = Depends(get_db),
):
    try:
        return partner_service.update_partner(db, partner_id, payload)
    except PartnerNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except PartnerSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except PartnerTypeNotFoundError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.delete("/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partner(partner_id: UUID, db: Session = Depends(get_db)):
    try:
        partner_service.delete_partner(db, partner_id)
    except PartnerNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
