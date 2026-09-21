from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.purchase_order import (
    LatestPurchaseOrderNumber,
    PurchaseOrderCreate,
    PurchaseOrderLineCreate,
    PurchaseOrderLineRead,
    PurchaseOrderLineUpdate,
    PurchaseOrderRead,
    PurchaseOrderUpdate,
)
from app.services import purchase_order as po_service
from app.services.purchase_order import (
    PurchaseOrderBrandNotFoundError,
    PurchaseOrderDateRangeError,
    PurchaseOrderItemNotFoundError,
    PurchaseOrderLineNotFoundError,
    PurchaseOrderLineNumberConflictError,
    PurchaseOrderNotFoundError,
    PurchaseOrderNumberConflictError,
    PurchaseOrderPartnerNotFoundError,
    PurchaseOrderUnitOfMeasureNotFoundError,
)

router = APIRouter(prefix="/purchase-orders", tags=["purchase orders"])


# ⚠️ /latest-number MUST be declared before /{purchase_order_id}
@router.get("/latest-number", response_model=LatestPurchaseOrderNumber)
def get_latest_number(db: Session = Depends(get_db)):
    return po_service.get_latest_number(db)


@router.get("", response_model=list[PurchaseOrderRead])
def list_purchase_orders(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return po_service.list_purchase_orders(db, limit=limit, offset=offset)


@router.get("/{purchase_order_id}", response_model=PurchaseOrderRead)
def get_purchase_order(
    purchase_order_id: UUID, db: Session = Depends(get_db)
):
    try:
        return po_service.get_purchase_order(db, purchase_order_id)
    except PurchaseOrderNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "",
    response_model=PurchaseOrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_purchase_order(
    payload: PurchaseOrderCreate, db: Session = Depends(get_db)
):
    try:
        return po_service.create_purchase_order(db, payload)
    except PurchaseOrderNumberConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (
        PurchaseOrderPartnerNotFoundError,
        PurchaseOrderBrandNotFoundError,
        PurchaseOrderItemNotFoundError,
        PurchaseOrderUnitOfMeasureNotFoundError,
        PurchaseOrderDateRangeError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.patch("/{purchase_order_id}", response_model=PurchaseOrderRead)
def update_purchase_order(
    purchase_order_id: UUID,
    payload: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
):
    try:
        return po_service.update_purchase_order(
            db, purchase_order_id, payload
        )
    except PurchaseOrderNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (
        PurchaseOrderPartnerNotFoundError,
        PurchaseOrderDateRangeError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete(
    "/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_purchase_order(
    purchase_order_id: UUID, db: Session = Depends(get_db)
):
    try:
        po_service.delete_purchase_order(db, purchase_order_id)
    except PurchaseOrderNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


# ── Line endpoints ────────────────────────────────────────────────────────────

@router.post(
    "/{purchase_order_id}/lines",
    response_model=PurchaseOrderLineRead,
    status_code=status.HTTP_201_CREATED,
)
def add_line(
    purchase_order_id: UUID,
    payload: PurchaseOrderLineCreate,
    db: Session = Depends(get_db),
):
    try:
        return po_service.add_line(db, purchase_order_id, payload)
    except PurchaseOrderNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (
        PurchaseOrderItemNotFoundError,
        PurchaseOrderUnitOfMeasureNotFoundError,
        PurchaseOrderLineNumberConflictError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.patch(
    "/{purchase_order_id}/lines/{line_id}",
    response_model=PurchaseOrderLineRead,
)
def update_line(
    purchase_order_id: UUID,
    line_id: UUID,
    payload: PurchaseOrderLineUpdate,
    db: Session = Depends(get_db),
):
    try:
        return po_service.update_line(
            db, purchase_order_id, line_id, payload
        )
    except PurchaseOrderLineNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (
        PurchaseOrderItemNotFoundError,
        PurchaseOrderUnitOfMeasureNotFoundError,
    ) as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


@router.delete(
    "/{purchase_order_id}/lines/{line_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_line(
    purchase_order_id: UUID,
    line_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        po_service.delete_line(db, purchase_order_id, line_id)
    except PurchaseOrderLineNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
