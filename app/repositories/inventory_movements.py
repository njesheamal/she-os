from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_movement import InventoryMovement


def get(db: Session, movement_id: UUID) -> InventoryMovement | None:
    return db.get(InventoryMovement, movement_id)


def list_all(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    item_id: UUID | None = None,
    inventory_location_id: UUID | None = None,
    occurred_from: datetime | None = None,
    occurred_until: datetime | None = None,
) -> list[InventoryMovement]:
    query = select(InventoryMovement)

    if item_id is not None:
        query = query.where(InventoryMovement.item_id == item_id)
    if inventory_location_id is not None:
        query = query.where(
            InventoryMovement.inventory_location_id == inventory_location_id
        )
    if occurred_from is not None:
        query = query.where(InventoryMovement.occurred_at >= occurred_from)
    if occurred_until is not None:
        query = query.where(InventoryMovement.occurred_at <= occurred_until)

    query = query.order_by(
        InventoryMovement.occurred_at.desc()
    ).limit(limit).offset(offset)

    return list(db.scalars(query))


def create(
    db: Session, movement: InventoryMovement
) -> InventoryMovement:
    db.add(movement)
    db.flush()
    db.refresh(movement)
    return movement
