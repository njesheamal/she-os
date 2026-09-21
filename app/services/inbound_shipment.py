from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import brand_inbound_shipments
from app.models.inbound_shipment import InboundShipment
from app.models.inbound_shipment_line import InboundShipmentLine
from app.repositories import inbound_shipment as shipment_repo
from app.schemas.inbound_shipment import (
    InboundShipmentCreate,
    InboundShipmentLineCreate,
    InboundShipmentLineRead,
    InboundShipmentLineUpdate,
    InboundShipmentRead,
    InboundShipmentUpdate,
    LatestInboundShipmentNumber,
)


class InboundShipmentNotFoundError(Exception):
    """No inbound shipment exists with the given identifier."""


class InboundShipmentLineNotFoundError(Exception):
    """No inbound shipment line exists with the given identifier."""


class InboundShipmentNumberConflictError(Exception):
    """An inbound shipment with this number already exists."""


class InboundShipmentBrandNotFoundError(Exception):
    """One or more of the referenced brands do not exist."""


class InboundShipmentLocationNotFoundError(Exception):
    """The referenced inventory location does not exist."""


class InboundShipmentPOLineNotFoundError(Exception):
    """The referenced purchase order line does not exist."""


class InboundShipmentPOLineConflictError(Exception):
    """This purchase order line is already on this shipment."""


class InboundShipmentUnitOfMeasureNotFoundError(Exception):
    """The referenced unit of measure does not exist."""


class InboundShipmentDateRangeError(Exception):
    """received_at occurs before shipped_at."""


def _raise_conflict(
    exc: IntegrityError,
    inbound_shipment_number: str | None = None,
    purchase_order_line_id: UUID | None = None,
    unit_of_measure_id: UUID | None = None,
) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "inbound_shipment_number" in constraint:
        raise InboundShipmentNumberConflictError(
            f"An inbound shipment with number "
            f"'{inbound_shipment_number}' already exists"
        ) from exc
    if "brand_id" in constraint:
        raise InboundShipmentBrandNotFoundError(
            "One or more of the referenced brand IDs do not exist"
        ) from exc
    if "destination_inventory_location_id" in constraint:
        raise InboundShipmentLocationNotFoundError(
            "The referenced inventory location does not exist"
        ) from exc
    if "shipment_po_line_unique" in constraint:
        raise InboundShipmentPOLineConflictError(
            f"Purchase order line {purchase_order_line_id} "
            f"is already on this shipment"
        ) from exc
    if "purchase_order_line_id" in constraint:
        raise InboundShipmentPOLineNotFoundError(
            f"No purchase order line found with ID {purchase_order_line_id}"
        ) from exc
    if "unit_of_measure_id" in constraint:
        raise InboundShipmentUnitOfMeasureNotFoundError(
            f"No unit of measure found with ID {unit_of_measure_id}"
        ) from exc
    if "dates_ordered" in constraint:
        raise InboundShipmentDateRangeError(
            "received_at must not occur before shipped_at"
        ) from exc
    raise


def _to_read(
    db: Session, shipment: InboundShipment
) -> InboundShipmentRead:
    """Assemble an InboundShipmentRead from ORM object plus queries."""
    brand_ids = shipment_repo.get_brand_ids(db, shipment.id)
    lines = shipment_repo.list_lines(db, shipment.id)
    return InboundShipmentRead.model_validate({
        "id": shipment.id,
        "inbound_shipment_number": shipment.inbound_shipment_number,
        "status": shipment.status,
        "tracking_number": shipment.tracking_number,
        "carrier_name": shipment.carrier_name,
        "destination_inventory_location_id": (
            shipment.destination_inventory_location_id
        ),
        "shipped_at": shipment.shipped_at,
        "received_at": shipment.received_at,
        "notes": shipment.notes,
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at,
        "brand_ids": brand_ids,
        "lines": [
            InboundShipmentLineRead.model_validate(line) for line in lines
        ],
    })


def _get_line_or_raise(
    db: Session, shipment_id: UUID, line_id: UUID
) -> InboundShipmentLine:
    line = shipment_repo.get_line(db, line_id)
    if line is None or line.inbound_shipment_id != shipment_id:
        raise InboundShipmentLineNotFoundError(
            f"No line found with ID {line_id} "
            f"on inbound shipment {shipment_id}"
        )
    return line


# ── Latest number ─────────────────────────────────────────────────────────────

def get_latest_number(db: Session) -> LatestInboundShipmentNumber:
    latest = shipment_repo.get_latest_number(db)
    suggested = shipment_repo.suggest_next_number(latest)
    return LatestInboundShipmentNumber(
        latest_inbound_shipment_number=latest,
        suggested_next=suggested,
    )


# ── Inbound shipment CRUD ─────────────────────────────────────────────────────

def get_inbound_shipment(
    db: Session, shipment_id: UUID
) -> InboundShipmentRead:
    shipment = shipment_repo.get(db, shipment_id)
    if shipment is None:
        raise InboundShipmentNotFoundError(
            f"No inbound shipment found with ID {shipment_id}"
        )
    return _to_read(db, shipment)


def list_inbound_shipments(
    db: Session, limit: int = 100, offset: int = 0
) -> list[InboundShipmentRead]:
    shipments = shipment_repo.list_all(db, limit=limit, offset=offset)
    return [_to_read(db, s) for s in shipments]


def create_inbound_shipment(
    db: Session, payload: InboundShipmentCreate
) -> InboundShipmentRead:
    shipment = InboundShipment(
        inbound_shipment_number=payload.inbound_shipment_number,
        status=payload.status,
        tracking_number=payload.tracking_number,
        carrier_name=payload.carrier_name,
        destination_inventory_location_id=(
            payload.destination_inventory_location_id
        ),
        shipped_at=payload.shipped_at,
        received_at=payload.received_at,
        notes=payload.notes,
    )

    try:
        shipment = shipment_repo.create(db, shipment)

        for brand_id in payload.brand_ids:
            db.execute(
                brand_inbound_shipments.insert().values(
                    brand_id=brand_id,
                    inbound_shipment_id=shipment.id,
                )
            )

        for line_payload in payload.lines:
            line = InboundShipmentLine(
                inbound_shipment_id=shipment.id,
                purchase_order_line_id=line_payload.purchase_order_line_id,
                quantity_shipped=line_payload.quantity_shipped,
                unit_of_measure_id=line_payload.unit_of_measure_id,
                notes=line_payload.notes,
            )
            db.add(line)

        db.flush()
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            inbound_shipment_number=payload.inbound_shipment_number,
        )

    db.refresh(shipment)
    return _to_read(db, shipment)


def update_inbound_shipment(
    db: Session, shipment_id: UUID, payload: InboundShipmentUpdate
) -> InboundShipmentRead:
    shipment = shipment_repo.get(db, shipment_id)
    if shipment is None:
        raise InboundShipmentNotFoundError(
            f"No inbound shipment found with ID {shipment_id}"
        )

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(shipment, field, value)

    try:
        shipment = shipment_repo.update(db, shipment)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            inbound_shipment_number=shipment.inbound_shipment_number,
        )

    db.refresh(shipment)
    return _to_read(db, shipment)


def delete_inbound_shipment(
    db: Session, shipment_id: UUID
) -> None:
    shipment = shipment_repo.get(db, shipment_id)
    if shipment is None:
        raise InboundShipmentNotFoundError(
            f"No inbound shipment found with ID {shipment_id}"
        )
    shipment_repo.delete(db, shipment)
    db.commit()


# ── Line CRUD ─────────────────────────────────────────────────────────────────

def add_line(
    db: Session,
    shipment_id: UUID,
    payload: InboundShipmentLineCreate,
) -> InboundShipmentLineRead:
    shipment = shipment_repo.get(db, shipment_id)
    if shipment is None:
        raise InboundShipmentNotFoundError(
            f"No inbound shipment found with ID {shipment_id}"
        )

    line = InboundShipmentLine(
        inbound_shipment_id=shipment_id,
        purchase_order_line_id=payload.purchase_order_line_id,
        quantity_shipped=payload.quantity_shipped,
        unit_of_measure_id=payload.unit_of_measure_id,
        notes=payload.notes,
    )

    try:
        line = shipment_repo.create_line(db, line)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            purchase_order_line_id=payload.purchase_order_line_id,
            unit_of_measure_id=payload.unit_of_measure_id,
        )

    db.refresh(line)
    return InboundShipmentLineRead.model_validate(line)


def update_line(
    db: Session,
    shipment_id: UUID,
    line_id: UUID,
    payload: InboundShipmentLineUpdate,
) -> InboundShipmentLineRead:
    line = _get_line_or_raise(db, shipment_id, line_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(line, field, value)

    try:
        line = shipment_repo.update_line(db, line)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            unit_of_measure_id=changes.get("unit_of_measure_id"),
        )

    db.refresh(line)
    return InboundShipmentLineRead.model_validate(line)


def delete_line(
    db: Session, shipment_id: UUID, line_id: UUID
) -> None:
    line = _get_line_or_raise(db, shipment_id, line_id)
    shipment_repo.delete_line(db, line)
    db.commit()
