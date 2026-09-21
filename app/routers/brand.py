from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.services import brand as brand_service
from app.services.brand import (
    BrandNameConflictError,
    BrandNotFoundError,
    BrandSlugConflictError,
)

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=list[BrandRead])
def list_brands(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return brand_service.list_brands(db, limit=limit, offset=offset)


@router.get("/{brand_id}", response_model=BrandRead)
def get_brand(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return brand_service.get_brand(db, brand_id)
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
def create_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    try:
        return brand_service.create_brand(db, payload)
    except (BrandSlugConflictError, BrandNameConflictError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.patch("/{brand_id}", response_model=BrandRead)
def update_brand(
    brand_id: UUID,
    payload: BrandUpdate,
    db: Session = Depends(get_db),
):
    try:
        return brand_service.update_brand(db, brand_id, payload)
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (BrandSlugConflictError, BrandNameConflictError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        brand_service.delete_brand(db, brand_id)
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
