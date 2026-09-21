import re
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.associations import brand_purchase_orders
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_line import PurchaseOrderLine

NUMBER_PATTERN = re.compile(r"^(?P<prefix>.*?)(?P<digits>\d+)$")


# ── Purchase order ────────────────────────────────────────────────────────────

def get(db: Session, purchase_order_id: UUID) -> PurchaseOrder | None:
    return db.get(PurchaseOrder, purchase_order_id)


def get_by_number(
    db: Session, purchase_order_number: str
) -> PurchaseOrder | None:
    return db.scalar(
        select(PurchaseOrder).where(
            PurchaseOrder.purchase_order_number == purchase_order_number
        )
    )


def list_all(
    db: Session, limit: int = 100, offset: int = 0
) -> list[PurchaseOrder]:
    return list(
        db.scalars(
            select(PurchaseOrder)
            .order_by(PurchaseOrder.order_date.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def get_latest_number(db: Session) -> str | None:
    """Most recently created purchase order number, estate-wide."""
    return db.scalar(
        select(PurchaseOrder.purchase_order_number)
        .order_by(PurchaseOrder.created_at.desc())
        .limit(1)
    )


def suggest_next_number(latest: str | None) -> str | None:
    """Increment trailing digits of the latest number, preserving padding."""
    if latest is None:
        return None
    match = NUMBER_PATTERN.match(latest)
    if match is None:
        return None
    prefix = match.group("prefix")
    digits = match.group("digits")
    incremented = str(int(digits) + 1).zfill(len(digits))
    return f"{prefix}{incremented}"


def get_brand_ids(db: Session, purchase_order_id: UUID) -> list[UUID]:
    """Load brand associations for a purchase order."""
    rows = db.execute(
        select(brand_purchase_orders.c.brand_id).where(
            brand_purchase_orders.c.purchase_order_id == purchase_order_id
        )
    ).scalars()
    return list(rows)


def create(db: Session, purchase_order: PurchaseOrder) -> PurchaseOrder:
    db.add(purchase_order)
    db.flush()
    db.refresh(purchase_order)
    return purchase_order


def update(db: Session, purchase_order: PurchaseOrder) -> PurchaseOrder:
    db.add(purchase_order)
    db.flush()
    db.refresh(purchase_order)
    return purchase_order


def delete(db: Session, purchase_order: PurchaseOrder) -> None:
    db.delete(purchase_order)
    db.flush()


# ── Lines ─────────────────────────────────────────────────────────────────────

def get_line(
    db: Session, line_id: UUID
) -> PurchaseOrderLine | None:
    return db.get(PurchaseOrderLine, line_id)


def list_lines(
    db: Session, purchase_order_id: UUID
) -> list[PurchaseOrderLine]:
    return list(
        db.scalars(
            select(PurchaseOrderLine)
            .where(
                PurchaseOrderLine.purchase_order_id == purchase_order_id
            )
            .order_by(PurchaseOrderLine.line_number)
        )
    )


def get_next_line_number(db: Session, purchase_order_id: UUID) -> int:
    """Return the next available line number for a purchase order."""
    from sqlalchemy import func
    current_max = db.scalar(
        select(func.max(PurchaseOrderLine.line_number)).where(
            PurchaseOrderLine.purchase_order_id == purchase_order_id
        )
    )
    return 1 if current_max is None else current_max + 1


def create_line(
    db: Session, line: PurchaseOrderLine
) -> PurchaseOrderLine:
    db.add(line)
    db.flush()
    db.refresh(line)
    return line


def update_line(
    db: Session, line: PurchaseOrderLine
) -> PurchaseOrderLine:
    db.add(line)
    db.flush()
    db.refresh(line)
    return line


def delete_line(db: Session, line: PurchaseOrderLine) -> None:
    db.delete(line)
    db.flush()
