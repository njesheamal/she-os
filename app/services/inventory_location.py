from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.inventory_location import InventoryLocation
from app.repositories import inventory_location as location_repo
from app.schemas.inventory_location import (
    InventoryLocationCreate,
    InventoryLocationUpdate,
)


class InventoryLocationNotFoundError(Exception):
    """No inventory location exists with the given identifier."""
 

class InventoryLocationSlugConflictError(Exception):
    """An inventory location with this slug already exists."""


class InventoryLocationTypeNotFoundError(Exception):
    """The referenced inventory location type does not exist."""


class InventoryLocationDateRangeError(Exception):
    """active_until occurs before active_from."""


def _raise_conflict(
    exc: IntegrityError,
    slug: str | None,
    location_type_id: UUID | None,
) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "inventory_location_type_id" in constraint:
        raise InventoryLocationTypeNotFoundError(
            f"No inventory location type found with ID {location_type_id}"
        ) from exc
    if "slug" in constraint:
        raise InventoryLocationSlugConflictError(
            f"An inventory location with slug '{slug}' already exists"
        ) from exc
    if "active_dates_ordered" in constraint:
        raise InventoryLocationDateRangeError(
            "active_until must not occur before active_from"
        ) from exc
    raise


def get_inventory_location(
    db: Session, location_id: UUID
) -> InventoryLocation:
    location = location_repo.get(db, location_id)
    if location is None:
        raise InventoryLocationNotFoundError(
            f"No inventory location found with ID {location_id}"
        )
    return location


def list_inventory_locations(
    db: Session, limit: int = 100, offset: int = 0
) -> list[InventoryLocation]:
    return location_repo.list_all(db, limit=limit, offset=offset)


def create_inventory_location(
    db: Session, payload: InventoryLocationCreate
) -> InventoryLocation:
    location = InventoryLocation(
        inventory_location_type_id=payload.inventory_location_type_id,
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        status=payload.status,
        address_line_1=payload.address_line_1,
        address_line_2=payload.address_line_2,
        city=payload.city,
        region=payload.region,
        postal_code=payload.postal_code,
        country_code=payload.country_code,
        active_from=payload.active_from,
        active_until=payload.active_until,
    )

    try:
        location = location_repo.create(db, location)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=payload.slug,
            location_type_id=payload.inventory_location_type_id,
        )

    db.refresh(location)
    return location


def update_inventory_location(
    db: Session, location_id: UUID, payload: InventoryLocationUpdate
) -> InventoryLocation:
    location = get_inventory_location(db, location_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(location, field, value)

    try:
        location = location_repo.update(db, location)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=changes.get("slug"),
            location_type_id=changes.get("inventory_location_type_id"),
        )

    db.refresh(location)
    return location


def delete_inventory_location(db: Session, location_id: UUID) -> None:
    location = get_inventory_location(db, location_id)
    location_repo.delete(db, location)
    db.commit()
