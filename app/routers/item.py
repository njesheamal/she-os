from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services import item as item_service
from app.services.item import (
    ItemNotFoundError,
    ItemSkuConflictError,
    ItemSlugConflictError,
    ItemTypeNotFoundError,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return item_service.list_items(db, limit=limit, offset=offset)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: UUID, db: Session = Depends(get_db)):
    try:
        return item_service.get_item(db, item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    try:
        return item_service.create_item(db, payload)
    except (ItemSlugConflictError, ItemSkuConflictError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ItemTypeNotFoundError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: UUID,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
):
    try:
        return item_service.update_item(db, item_id, payload)
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (ItemSlugConflictError, ItemSkuConflictError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ItemTypeNotFoundError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: UUID, db: Session = Depends(get_db)):
    try:
        item_service.delete_item(db, item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
