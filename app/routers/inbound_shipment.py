from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.inbound_shipment import (
    InboundShipmentCreate,
    InboundShipmentLineCreate,
    InboundShipmentLineRead,
    InboundShipmentLineUpdate,
    InboundShipmentRead,
    InboundShipmentUpdate,
    LatestInboundShipmentNumber,
)
from app.services import inbound_shipment as shipment_service
from app.services.inbound_shipment import (
    InboundShipmentBrandNotFoundError,
    InboundShipmentDateRangeError,
    InboundShipmentLineNotFoundError,
    InboundShipmentLocationNotFoundError,
    InboundShipmentNotFoundError,
    InboundShipmentNumberConflictError,
    InboundShipmentPOLineConflictError,
    InboundShipmentPOLineNotFoundError,
    InboundShipmentUnitOfMeasureNotFoundError,
)

router = APIRouter(
    prefix="/inbound-shipments", tags=["inbound shipments"]
)


# ⚠️ /latest-number before /{shipment_id}
@router.get(
    "/latest-number", response_model=LatestInboundShipmentNumber
)
def get_latest_number(db: Session = Depends(get_db)):
    return shipment_service.get_latest_number(db)


@router.get("", response_model=list[InboundShipmentRead])
def list_inbound_shipments(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return shipment_service.list_inbound_shipments(
        db, limit=limit, offset=offset
    )


@router.get("/{shipment_id}", response_model=InboundShipmentRead)
def get_inbound_shipment(
    shipment_id: UUID, db: Session = Depends(get_db)
):
    try:
        return shipment_service.get_inbound_shipment(db, shipment_id)
    except InboundShipmentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "",
    response_model=InboundShipmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_inbound_shipment(
    payload: InboundShipmentCreate, db: Session = Depends(get_db)
):
    try:
        return shipment_service.create_inbound_shipment(db, payload)
    except InboundShipmentNumberConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (
        InboundShipmentBrandNotFoundError,
        InboundShipmentLocationNotFoundError,
        InboundShipmentPOLineNotFoundError,
        InboundShipmentPOLineConflictError,
        InboundShipmentUnitOfMeasureNotFoundError,
        InboundShipmentDateRangeError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.patch("/{shipment_id}", response_model=InboundShipmentRead)
def update_inbound_shipment(
    shipment_id: UUID,
    payload: InboundShipmentUpdate,
    db: Session = Depends(get_db),
):
    try:
        return shipment_service.update_inbound_shipment(
            db, shipment_id, payload
        )
    except InboundShipmentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (
        InboundShipmentLocationNotFoundError,
        InboundShipmentDateRangeError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inbound_shipment(
    shipment_id: UUID, db: Session = Depends(get_db)
):
    try:
        shipment_service.delete_inbound_shipment(db, shipment_id)
    except InboundShipmentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


# ── Line endpoints ────────────────────────────────────────────────────────────

@router.post(
    "/{shipment_id}/lines",
    response_model=InboundShipmentLineRead,
    status_code=status.HTTP_201_CREATED,
)
def add_line(
    shipment_id: UUID,
    payload: InboundShipmentLineCreate,
    db: Session = Depends(get_db),
):
    try:
        return shipment_service.add_line(db, shipment_id, payload)
    except InboundShipmentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (
        InboundShipmentPOLineNotFoundError,
        InboundShipmentUnitOfMeasureNotFoundError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc
    except InboundShipmentPOLineConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.patch(
    "/{shipment_id}/lines/{line_id}",
    response_model=InboundShipmentLineRead,
)
def update_line(
    shipment_id: UUID,
    line_id: UUID,
    payload: InboundShipmentLineUpdate,
    db: Session = Depends(get_db),
):
    try:
        return shipment_service.update_line(
            db, shipment_id, line_id, payload
        )
    except InboundShipmentLineNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InboundShipmentUnitOfMeasureNotFoundError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete(
    "/{shipment_id}/lines/{line_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_line(
    shipment_id: UUID,
    line_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        shipment_service.delete_line(db, shipment_id, line_id)
    except InboundShipmentLineNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
