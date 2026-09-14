from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.inventory_location import (
    InventoryLocationCreate,
    InventoryLocationRead,
    InventoryLocationUpdate,
)
from app.services import inventory_location as location_service
from app.services.inventory_location import (
    InventoryLocationDateRangeError,
    InventoryLocationNotFoundError,
    InventoryLocationSlugConflictError,
    InventoryLocationTypeNotFoundError,
)

router = APIRouter(
    prefix="/inventory-locations", tags=["inventory locations"]
)


@router.get("", response_model=list[InventoryLocationRead])
def list_inventory_locations(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return location_service.list_inventory_locations(
        db, limit=limit, offset=offset
    )


@router.get("/{location_id}", response_model=InventoryLocationRead)
def get_inventory_location(location_id: UUID, db: Session = Depends(get_db)):
    try:
        return location_service.get_inventory_location(db, location_id)
    except InventoryLocationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "",
    response_model=InventoryLocationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory_location(
    payload: InventoryLocationCreate, db: Session = Depends(get_db)
):
    try:
        return location_service.create_inventory_location(db, payload)
    except InventoryLocationSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (
        InventoryLocationTypeNotFoundError,
        InventoryLocationDateRangeError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.patch("/{location_id}", response_model=InventoryLocationRead)
def update_inventory_location(
    location_id: UUID,
    payload: InventoryLocationUpdate,
    db: Session = Depends(get_db),
):
    try:
        return location_service.update_inventory_location(
            db, location_id, payload
        )
    except InventoryLocationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InventoryLocationSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (
        InventoryLocationTypeNotFoundError,
        InventoryLocationDateRangeError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_location(
    location_id: UUID, db: Session = Depends(get_db)
):
    try:
        location_service.delete_inventory_location(db, location_id)
    except InventoryLocationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
