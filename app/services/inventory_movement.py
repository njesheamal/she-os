from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.inventory_movement import InventoryMovement
from app.repositories import inventory_balance as balance_repo
from app.repositories import inventory_movements as movement_repo
from app.schemas.inventory_balance import InventoryBalanceRead
from app.schemas.inventory_movement import (
    InventoryMovementCreate,
    InventoryMovementRead,
)


class InventoryMovementNotFoundError(Exception):
    """No inventory movement exists with the given identifier."""


class InventoryMovementItemNotFoundError(Exception):
    """The referenced item does not exist."""


class InventoryMovementLocationNotFoundError(Exception):
    """The referenced inventory location does not exist."""


class InventoryMovementTypeNotFoundError(Exception):
    """The referenced inventory movement type does not exist."""


class InventoryMovementUnitNotFoundError(Exception):
    """The referenced unit of measure does not exist."""


class InventoryMovementZeroDeltaError(Exception):
    """quantity_delta must not be zero."""


class InventoryBalanceWouldGoNegativeError(Exception):
    """This movement would push the balance below zero."""


def _raise_conflict(exc: IntegrityError) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "item_id" in constraint:
        raise InventoryMovementItemNotFoundError(
            "The referenced item does not exist"
        ) from exc
    if "inventory_location_id" in constraint:
        raise InventoryMovementLocationNotFoundError(
            "The referenced inventory location does not exist"
        ) from exc
    if "inventory_movement_type_id" in constraint:
        raise InventoryMovementTypeNotFoundError(
            "The referenced inventory movement type does not exist"
        ) from exc
    if "unit_of_measure_id" in constraint:
        raise InventoryMovementUnitNotFoundError(
            "The referenced unit of measure does not exist"
        ) from exc
    if "quantity_on_hand" in constraint:
        raise InventoryBalanceWouldGoNegativeError(
            "This movement would push the balance below zero"
        ) from exc
    raise


def get_movement(
    db: Session, movement_id: UUID
) -> InventoryMovementRead:
    movement = movement_repo.get(db, movement_id)
    if movement is None:
        raise InventoryMovementNotFoundError(
            f"No inventory movement found with ID {movement_id}"
        )
    return InventoryMovementRead.model_validate(movement)


def list_movements(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    item_id: UUID | None = None,
    inventory_location_id: UUID | None = None,
    occurred_from: datetime | None = None,
    occurred_until: datetime | None = None,
) -> list[InventoryMovementRead]:
    movements = movement_repo.list_all(
        db,
        limit=limit,
        offset=offset,
        item_id=item_id,
        inventory_location_id=inventory_location_id,
        occurred_from=occurred_from,
        occurred_until=occurred_until,
    )
    return [InventoryMovementRead.model_validate(m) for m in movements]


def post_movement(
    db: Session, payload: InventoryMovementCreate
) -> InventoryMovementRead:
    if payload.quantity_delta == Decimal("0"):
        raise InventoryMovementZeroDeltaError(
            "quantity_delta must not be zero"
        )

    if payload.quantity_delta < Decimal("0"):
        current = balance_repo.get(
            db,
            item_id=payload.item_id,
            inventory_location_id=payload.inventory_location_id,
        )
        current_qty = (
            current.quantity_on_hand if current is not None else Decimal("0")
        )
        if current_qty + payload.quantity_delta < Decimal("0"):
            raise InventoryBalanceWouldGoNegativeError(
                f"Movement of {payload.quantity_delta} would push balance "
                f"from {current_qty} to "
                f"{current_qty + payload.quantity_delta}"
            )

    movement = InventoryMovement(
        item_id=payload.item_id,
        inventory_location_id=payload.inventory_location_id,
        inventory_movement_type_id=payload.inventory_movement_type_id,
        inbound_shipment_line_id=payload.inbound_shipment_line_id,
        related_movement_id=payload.related_movement_id,
        quantity_delta=payload.quantity_delta,
        unit_of_measure_id=payload.unit_of_measure_id,
        occurred_at=payload.occurred_at,
        notes=payload.notes,
    )

    try:
        movement = movement_repo.create(db, movement)

        balance_repo.upsert(
            db,
            item_id=payload.item_id,
            inventory_location_id=payload.inventory_location_id,
            unit_of_measure_id=payload.unit_of_measure_id,
            quantity_delta=payload.quantity_delta,
        )

        db.commit()

    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc)

    db.refresh(movement)
    return InventoryMovementRead.model_validate(movement)


# ── Balance reads ─────────────────────────────────────────────────────────────

def list_balances(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    item_id: UUID | None = None,
    inventory_location_id: UUID | None = None,
) -> list[InventoryBalanceRead]:
    balances = balance_repo.list_all(
        db,
        limit=limit,
        offset=offset,
        item_id=item_id,
        inventory_location_id=inventory_location_id,
    )
    return [InventoryBalanceRead.model_validate(b) for b in balances]
