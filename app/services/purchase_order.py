from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import brand_purchase_orders
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_line import PurchaseOrderLine
from app.repositories import purchase_order as po_repo
from app.schemas.purchase_order import (
    LatestPurchaseOrderNumber,
    PurchaseOrderCreate,
    PurchaseOrderLineCreate,
    PurchaseOrderLineRead,
    PurchaseOrderLineUpdate,
    PurchaseOrderRead,
    PurchaseOrderUpdate,
)


class PurchaseOrderNotFoundError(Exception):
    """No purchase order exists with the given identifier."""


class PurchaseOrderLineNotFoundError(Exception):
    """No purchase order line exists with the given identifier."""


class PurchaseOrderNumberConflictError(Exception):
    """A purchase order with this number already exists."""


class PurchaseOrderPartnerNotFoundError(Exception):
    """The referenced partner does not exist."""


class PurchaseOrderBrandNotFoundError(Exception):
    """One or more of the referenced brands do not exist."""


class PurchaseOrderItemNotFoundError(Exception):
    """The referenced item does not exist."""


class PurchaseOrderUnitOfMeasureNotFoundError(Exception):
    """The referenced unit of measure does not exist."""


class PurchaseOrderDateRangeError(Exception):
    """expected_date occurs before order_date."""


class PurchaseOrderLineNumberConflictError(Exception):
    """A line with this number already exists on this purchase order."""


def _raise_conflict(
    exc: IntegrityError,
    purchase_order_number: str | None = None,
    partner_id: UUID | None = None,
    item_id: UUID | None = None,
    unit_of_measure_id: UUID | None = None,
) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "purchase_order_number" in constraint:
        raise PurchaseOrderNumberConflictError(
            f"A purchase order with number '{purchase_order_number}' already exists"
        ) from exc
    if "partner_id" in constraint:
        raise PurchaseOrderPartnerNotFoundError(
            f"No partner found with ID {partner_id}"
        ) from exc
    if "brand_id" in constraint:
        raise PurchaseOrderBrandNotFoundError(
            "One or more of the referenced brand IDs do not exist"
        ) from exc
    if "item_id" in constraint:
        raise PurchaseOrderItemNotFoundError(
            f"No item found with ID {item_id}"
        ) from exc
    if "unit_of_measure_id" in constraint:
        raise PurchaseOrderUnitOfMeasureNotFoundError(
            f"No unit of measure found with ID {unit_of_measure_id}"
        ) from exc
    if "dates_ordered" in constraint:
        raise PurchaseOrderDateRangeError(
            "expected_date must not occur before order_date"
        ) from exc
    if "po_line_number" in constraint:
        raise PurchaseOrderLineNumberConflictError(
            "A line with this number already exists on this purchase order"
        ) from exc
    raise


def _to_read(db: Session, po: PurchaseOrder) -> PurchaseOrderRead:
    """Assemble a PurchaseOrderRead from ORM object plus additional queries."""
    brand_ids = po_repo.get_brand_ids(db, po.id)
    lines = po_repo.list_lines(db, po.id)
    return PurchaseOrderRead.model_validate({
        "id": po.id,
        "purchase_order_number": po.purchase_order_number,
        "partner_id": po.partner_id,
        "status": po.status,
        "order_date": po.order_date,
        "expected_date": po.expected_date,
        "currency_code": po.currency_code,
        "production_brief": po.production_brief,
        "notes": po.notes,
        "created_at": po.created_at,
        "updated_at": po.updated_at,
        "brand_ids": brand_ids,
        "lines": [
            PurchaseOrderLineRead.model_validate(line) for line in lines
        ],
    })


def _get_line_or_raise(
    db: Session, purchase_order_id: UUID, line_id: UUID
) -> PurchaseOrderLine:
    line = po_repo.get_line(db, line_id)
    if line is None or line.purchase_order_id != purchase_order_id:
        raise PurchaseOrderLineNotFoundError(
            f"No line found with ID {line_id} "
            f"on purchase order {purchase_order_id}"
        )
    return line


# ── Latest number ─────────────────────────────────────────────────────────────

def get_latest_number(db: Session) -> LatestPurchaseOrderNumber:
    latest = po_repo.get_latest_number(db)
    suggested = po_repo.suggest_next_number(latest)
    return LatestPurchaseOrderNumber(
        latest_purchase_order_number=latest,
        suggested_next=suggested,
    )


# ── Purchase order CRUD ───────────────────────────────────────────────────────

def get_purchase_order(
    db: Session, purchase_order_id: UUID
) -> PurchaseOrderRead:
    po = po_repo.get(db, purchase_order_id)
    if po is None:
        raise PurchaseOrderNotFoundError(
            f"No purchase order found with ID {purchase_order_id}"
        )
    return _to_read(db, po)


def list_purchase_orders(
    db: Session, limit: int = 100, offset: int = 0
) -> list[PurchaseOrderRead]:
    pos = po_repo.list_all(db, limit=limit, offset=offset)
    return [_to_read(db, po) for po in pos]


def create_purchase_order(
    db: Session, payload: PurchaseOrderCreate
) -> PurchaseOrderRead:
    po = PurchaseOrder(
        purchase_order_number=payload.purchase_order_number,
        partner_id=payload.partner_id,
        status=payload.status,
        order_date=payload.order_date,
        expected_date=payload.expected_date,
        currency_code=payload.currency_code,
        production_brief=payload.production_brief,
        notes=payload.notes,
    )

    try:
        po = po_repo.create(db, po)

        for brand_id in payload.brand_ids:
            db.execute(
                brand_purchase_orders.insert().values(
                    brand_id=brand_id,
                    purchase_order_id=po.id,
                )
            )

        for position, line_payload in enumerate(payload.lines, start=1):
            line = PurchaseOrderLine(
                purchase_order_id=po.id,
                item_id=line_payload.item_id,
                line_number=position,
                description=line_payload.description,
                quantity_ordered=line_payload.quantity_ordered,
                unit_of_measure_id=line_payload.unit_of_measure_id,
                unit_price=line_payload.unit_price,
            )
            db.add(line)

        db.flush()
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            purchase_order_number=payload.purchase_order_number,
            partner_id=payload.partner_id,
        )

    db.refresh(po)
    return _to_read(db, po)


def update_purchase_order(
    db: Session, purchase_order_id: UUID, payload: PurchaseOrderUpdate
) -> PurchaseOrderRead:
    po = po_repo.get(db, purchase_order_id)
    if po is None:
        raise PurchaseOrderNotFoundError(
            f"No purchase order found with ID {purchase_order_id}"
        )

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(po, field, value)

    try:
        po = po_repo.update(db, po)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            partner_id=changes.get("partner_id"),
        )

    db.refresh(po)
    return _to_read(db, po)


def delete_purchase_order(
    db: Session, purchase_order_id: UUID
) -> None:
    po = po_repo.get(db, purchase_order_id)
    if po is None:
        raise PurchaseOrderNotFoundError(
            f"No purchase order found with ID {purchase_order_id}"
        )
    po_repo.delete(db, po)
    db.commit()


# ── Line CRUD ─────────────────────────────────────────────────────────────────

def add_line(
    db: Session,
    purchase_order_id: UUID,
    payload: PurchaseOrderLineCreate,
) -> PurchaseOrderLineRead:
    po = po_repo.get(db, purchase_order_id)
    if po is None:
        raise PurchaseOrderNotFoundError(
            f"No purchase order found with ID {purchase_order_id}"
        )

    line_number = po_repo.get_next_line_number(db, purchase_order_id)

    line = PurchaseOrderLine(
        purchase_order_id=purchase_order_id,
        item_id=payload.item_id,
        line_number=line_number,
        description=payload.description,
        quantity_ordered=payload.quantity_ordered,
        unit_of_measure_id=payload.unit_of_measure_id,
        unit_price=payload.unit_price,
    )

    try:
        line = po_repo.create_line(db, line)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            item_id=payload.item_id,
            unit_of_measure_id=payload.unit_of_measure_id,
        )

    db.refresh(line)
    return PurchaseOrderLineRead.model_validate(line)


def update_line(
    db: Session,
    purchase_order_id: UUID,
    line_id: UUID,
    payload: PurchaseOrderLineUpdate,
) -> PurchaseOrderLineRead:
    line = _get_line_or_raise(db, purchase_order_id, line_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(line, field, value)

    try:
        line = po_repo.update_line(db, line)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            item_id=changes.get("item_id"),
            unit_of_measure_id=changes.get("unit_of_measure_id"),
        )

    db.refresh(line)
    return PurchaseOrderLineRead.model_validate(line)


def delete_line(
    db: Session, purchase_order_id: UUID, line_id: UUID
) -> None:
    line = _get_line_or_raise(db, purchase_order_id, line_id)
    po_repo.delete_line(db, line)
    db.commit()
