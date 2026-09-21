from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_balance import InventoryBalance


def get(
    db: Session,
    item_id: UUID,
    inventory_location_id: UUID,
) -> InventoryBalance | None:
    return db.scalar(
        select(InventoryBalance).where(
            InventoryBalance.item_id == item_id,
            InventoryBalance.inventory_location_id == inventory_location_id,
        )
    )


def list_all(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    item_id: UUID | None = None,
    inventory_location_id: UUID | None = None,
) -> list[InventoryBalance]:
    query = select(InventoryBalance)

    if item_id is not None:
        query = query.where(InventoryBalance.item_id == item_id)
    if inventory_location_id is not None:
        query = query.where(
            InventoryBalance.inventory_location_id == inventory_location_id
        )

    query = query.order_by(InventoryBalance.updated_at.desc()) \
        .limit(limit).offset(offset)

    return list(db.scalars(query))


def upsert(
    db: Session,
    item_id: UUID,
    inventory_location_id: UUID,
    unit_of_measure_id: UUID,
    quantity_delta: object,
) -> InventoryBalance:
    """Apply a delta to the balance, creating the row if it doesn't exist."""
    from decimal import Decimal
    from sqlalchemy.dialects.postgresql import insert
    from app.models.inventory_balance import InventoryBalance

    stmt = insert(InventoryBalance).values(
        item_id=item_id,
        inventory_location_id=inventory_location_id,
        unit_of_measure_id=unit_of_measure_id,
        quantity_on_hand=quantity_delta,
    ).on_conflict_do_update(
        index_elements=["item_id", "inventory_location_id"],
        set_={
            "quantity_on_hand": (
                InventoryBalance.quantity_on_hand + quantity_delta
            ),
            "updated_at": db.execute(
                select(__import__("sqlalchemy").func.now())
            ).scalar(),
        },
    ).returning(InventoryBalance)

    result = db.execute(stmt)
    db.flush()
    return result.scalars().one()
