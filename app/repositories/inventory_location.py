from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_location import InventoryLocation


def get(db: Session, location_id: UUID) -> InventoryLocation | None:
    return db.get(InventoryLocation, location_id)


def get_by_slug(db: Session, slug: str) -> InventoryLocation | None:
    return db.scalar(
        select(InventoryLocation).where(InventoryLocation.slug == slug)
    )


def list_all(
    db: Session, limit: int = 100, offset: int = 0
) -> list[InventoryLocation]:
    return list(
        db.scalars(
            select(InventoryLocation)
            .order_by(InventoryLocation.name)
            .limit(limit)
            .offset(offset)
        )
    )


def create(db: Session, location: InventoryLocation) -> InventoryLocation:
    db.add(location)
    db.flush()
    db.refresh(location)
    return location


def update(db: Session, location: InventoryLocation) -> InventoryLocation:
    db.add(location)
    db.flush()
    db.refresh(location)
    return location


def delete(db: Session, location: InventoryLocation) -> None:
    db.delete(location)
    db.flush()
