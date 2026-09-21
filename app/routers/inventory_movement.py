from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.inventory_balance import InventoryBalanceRead
from app.schemas.inventory_movement import (
    InventoryMovementCreate,
    InventoryMovementRead,
)
from app.services import inventory_movement as movement_service
from app.services.inventory_movement import (
    InventoryBalanceWouldGoNegativeError,
    InventoryMovementItemNotFoundError,
    InventoryMovementLocationNotFoundError,
    InventoryMovementNotFoundError,
    InventoryMovementTypeNotFoundError,
    InventoryMovementUnitNotFoundError,
    InventoryMovementZeroDeltaError,
)

router = APIRouter(
    prefix="/inventory-movements", tags=["inventory movements"]
)

balances_router = APIRouter(
    prefix="/inventory-balances", tags=["inventory balances"]
)


@balances_router.get("", response_model=list[InventoryBalanceRead])
def list_balances(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    item_id: UUID | None = Query(default=None),
    inventory_location_id: UUID | None = Query(default=None),
):
    return movement_service.list_balances(
        db,
        limit=limit,
        offset=offset,
        item_id=item_id,
        inventory_location_id=inventory_location_id,
    )


@router.get("", response_model=list[InventoryMovementRead])
def list_movements(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    item_id: UUID | None = Query(default=None),
    inventory_location_id: UUID | None = Query(default=None),
    occurred_from: datetime | None = Query(default=None),
    occurred_until: datetime | None = Query(default=None),
):
    return movement_service.list_movements(
        db,
        limit=limit,
        offset=offset,
        item_id=item_id,
        inventory_location_id=inventory_location_id,
        occurred_from=occurred_from,
        occurred_until=occurred_until,
    )


@router.get("/{movement_id}", response_model=InventoryMovementRead)
def get_movement(movement_id: UUID, db: Session = Depends(get_db)):
    try:
        return movement_service.get_movement(db, movement_id)
    except InventoryMovementNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "",
    response_model=InventoryMovementRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Movement would push balance below zero"},
        422: {"description": "Validation error (e.g. missing item, location, type, or unit) or invalid reference (e.g. item, location, type, or unit does not exist)"},
    },
)
def post_movement(
    payload: InventoryMovementCreate, db: Session = Depends(get_db)
):
    try:
        return movement_service.post_movement(db, payload)
    except (
        InventoryMovementZeroDeltaError,
        InventoryMovementItemNotFoundError,
        InventoryMovementLocationNotFoundError,
        InventoryMovementTypeNotFoundError,
        InventoryMovementUnitNotFoundError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc
    except InventoryBalanceWouldGoNegativeError as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, str(exc)
        ) from exc
