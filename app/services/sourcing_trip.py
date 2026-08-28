from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.sourcing_trip import SourcingTrip
from app.repositories import sourcing_trip as trip_repo
from app.schemas.sourcing_trip import SourcingTripCreate, SourcingTripUpdate


class SourcingTripNotFoundError(Exception):
    """No sourcing trip exists with the given identifier."""


class SourcingTripSlugConflictError(Exception):
    """A sourcing trip with this slug already exists."""


class SourcingTripDateRangeError(Exception):
    """The end date occurs before the start date."""


def _raise_conflict(exc: IntegrityError, slug: str | None) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "slug" in constraint:
        raise SourcingTripSlugConflictError(
            f"A sourcing trip with slug '{slug}' already exists"
        ) from exc
    if "dates_ordered" in constraint:
        raise SourcingTripDateRangeError(
            "end_date must not occur before start_date"
        ) from exc
    raise


def get_sourcing_trip(db: Session, trip_id: UUID) -> SourcingTrip:
    trip = trip_repo.get(db, trip_id)
    if trip is None:
        raise SourcingTripNotFoundError(
            f"No sourcing trip found with ID {trip_id}"
        )
    return trip


def list_sourcing_trips(
    db: Session, limit: int = 100, offset: int = 0
) -> list[SourcingTrip]:
    return trip_repo.list_all(db, limit=limit, offset=offset)


def create_sourcing_trip(
    db: Session, payload: SourcingTripCreate
) -> SourcingTrip:
    trip = SourcingTrip(
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        status=payload.status,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )

    try:
        trip = trip_repo.create(db, trip)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc, slug=payload.slug)

    db.refresh(trip)
    return trip


def update_sourcing_trip(
    db: Session, trip_id: UUID, payload: SourcingTripUpdate
) -> SourcingTrip:
    trip = get_sourcing_trip(db, trip_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(trip, field, value)

    try:
        trip = trip_repo.update(db, trip)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc, slug=changes.get("slug"))

    db.refresh(trip)
    return trip


def delete_sourcing_trip(db: Session, trip_id: UUID) -> None:
    trip = get_sourcing_trip(db, trip_id)
    trip_repo.delete(db, trip)
    db.commit()
