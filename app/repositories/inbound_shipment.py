import re
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.associations import brand_inbound_shipments
from app.models.inbound_shipment import InboundShipment
from app.models.inbound_shipment_line import InboundShipmentLine

NUMBER_PATTERN = re.compile(r"^(?P<prefix>.*?)(?P<digits>\d+)$")


# ── Inbound shipment ──────────────────────────────────────────────────────────

def get(db: Session, shipment_id: UUID) -> InboundShipment | None:
    return db.get(InboundShipment, shipment_id)


def get_by_number(
    db: Session, inbound_shipment_number: str
) -> InboundShipment | None:
    return db.scalar(
        select(InboundShipment).where(
            InboundShipment.inbound_shipment_number == inbound_shipment_number
        )
    )


def list_all(
    db: Session, limit: int = 100, offset: int = 0
) -> list[InboundShipment]:
    return list(
        db.scalars(
            select(InboundShipment)
            .order_by(InboundShipment.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def get_latest_number(db: Session) -> str | None:
    """Most recently created inbound shipment number, estate-wide."""
    return db.scalar(
        select(InboundShipment.inbound_shipment_number)
        .order_by(InboundShipment.created_at.desc())
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


def get_brand_ids(db: Session, shipment_id: UUID) -> list[UUID]:
    """Load brand associations for a shipment."""
    rows = db.execute(
        select(brand_inbound_shipments.c.brand_id).where(
            brand_inbound_shipments.c.inbound_shipment_id == shipment_id
        )
    ).scalars()
    return list(rows)


def create(
    db: Session, shipment: InboundShipment
) -> InboundShipment:
    db.add(shipment)
    db.flush()
    db.refresh(shipment)
    return shipment


def update(
    db: Session, shipment: InboundShipment
) -> InboundShipment:
    db.add(shipment)
    db.flush()
    db.refresh(shipment)
    return shipment


def delete(db: Session, shipment: InboundShipment) -> None:
    db.delete(shipment)
    db.flush()


# ── Lines ─────────────────────────────────────────────────────────────────────

def get_line(
    db: Session, line_id: UUID
) -> InboundShipmentLine | None:
    return db.get(InboundShipmentLine, line_id)


def list_lines(
    db: Session, shipment_id: UUID
) -> list[InboundShipmentLine]:
    return list(
        db.scalars(
            select(InboundShipmentLine)
            .where(InboundShipmentLine.inbound_shipment_id == shipment_id)
            .order_by(InboundShipmentLine.created_at)
        )
    )


def create_line(
    db: Session, line: InboundShipmentLine
) -> InboundShipmentLine:
    db.add(line)
    db.flush()
    db.refresh(line)
    return line


def update_line(
    db: Session, line: InboundShipmentLine
) -> InboundShipmentLine:
    db.add(line)
    db.flush()
    db.refresh(line)
    return line


def delete_line(db: Session, line: InboundShipmentLine) -> None:
    db.delete(line)
    db.flush()
