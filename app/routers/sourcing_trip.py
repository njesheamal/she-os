from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.sourcing_trip import (
    SourcingTripCreate,
    SourcingTripRead,
    SourcingTripUpdate,
)
from app.services import sourcing_trip as trip_service
from app.services.sourcing_trip import (
    SourcingTripDateRangeError,
    SourcingTripNotFoundError,
    SourcingTripSlugConflictError,
)

router = APIRouter(prefix="/sourcing-trips", tags=["sourcing trips"])


@router.get("", response_model=list[SourcingTripRead])
def list_sourcing_trips(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return trip_service.list_sourcing_trips(db, limit=limit, offset=offset)


@router.get("/{trip_id}", response_model=SourcingTripRead)
def get_sourcing_trip(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return trip_service.get_sourcing_trip(db, trip_id)
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "", response_model=SourcingTripRead, status_code=status.HTTP_201_CREATED
)
def create_sourcing_trip(
    payload: SourcingTripCreate, db: Session = Depends(get_db)
):
    try:
        return trip_service.create_sourcing_trip(db, payload)
    except SourcingTripSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except SourcingTripDateRangeError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.patch("/{trip_id}", response_model=SourcingTripRead)
def update_sourcing_trip(
    trip_id: UUID,
    payload: SourcingTripUpdate,
    db: Session = Depends(get_db),
):
    try:
        return trip_service.update_sourcing_trip(db, trip_id, payload)
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except SourcingTripSlugConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except SourcingTripDateRangeError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sourcing_trip(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        trip_service.delete_sourcing_trip(db, trip_id)
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
