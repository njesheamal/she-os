from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sourcing_trip import SourcingTrip


def get(db: Session, trip_id: UUID) -> SourcingTrip | None:
    return db.get(SourcingTrip, trip_id)


def get_by_slug(db: Session, slug: str) -> SourcingTrip | None:
    return db.scalar(select(SourcingTrip).where(SourcingTrip.slug == slug))


def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[SourcingTrip]:
    return list(
        db.scalars(
            select(SourcingTrip)
            .order_by(SourcingTrip.start_date.desc().nullslast())
            .limit(limit)
            .offset(offset)
        )
    )


def create(db: Session, trip: SourcingTrip) -> SourcingTrip:
    db.add(trip)
    db.flush()
    db.refresh(trip)
    return trip


def update(db: Session, trip: SourcingTrip) -> SourcingTrip:
    db.add(trip)
    db.flush()
    db.refresh(trip)
    return trip


def delete(db: Session, trip: SourcingTrip) -> None:
    db.delete(trip)
    db.flush()
