from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.decision import DecisionRead
from app.schemas.inbound_shipment import InboundShipmentRead
from app.schemas.item import ItemRead
from app.schemas.observation import ObservationRead
from app.schemas.partner import PartnerRead
from app.schemas.purchase_order import PurchaseOrderRead
from app.services.associations import sourcing_trip_associations as assoc_service
from app.services.decision import DecisionNotFoundError
from app.services.inbound_shipment import InboundShipmentNotFoundError
from app.services.observation import ObservationNotFoundError
from app.services.partner import PartnerNotFoundError
from app.services.purchase_order import PurchaseOrderNotFoundError
from app.services.sourcing_trip import SourcingTripNotFoundError

router = APIRouter(prefix="/sourcing-trips", tags=["sourcing trip associations"])


@router.get("/{trip_id}/items", response_model=list[ItemRead])
def list_trip_items(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return [ItemRead.model_validate(i) for i in assoc_service.get_items_for_sourcing_trip(db, trip_id)]
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{trip_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_trip_item(trip_id: UUID, item_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_item_to_sourcing_trip(db, trip_id, item_id)
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{trip_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_trip_item(trip_id: UUID, item_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_item_from_sourcing_trip(db, trip_id, item_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sourcing trip {trip_id} is not linked to item {item_id}")
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{trip_id}/partners", response_model=list[PartnerRead])
def list_trip_partners(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return [PartnerRead.model_validate(p) for p in assoc_service.get_partners_for_sourcing_trip(db, trip_id)]
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{trip_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_trip_partner(trip_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_partner_to_sourcing_trip(db, trip_id, partner_id)
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{trip_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_trip_partner(trip_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_partner_from_sourcing_trip(db, trip_id, partner_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sourcing trip {trip_id} is not linked to partner {partner_id}")
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{trip_id}/observations", response_model=list[ObservationRead])
def list_trip_observations(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return [ObservationRead.model_validate(o) for o in assoc_service.get_observations_for_sourcing_trip(db, trip_id)]
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{trip_id}/observations/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_trip_observation(trip_id: UUID, observation_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_observation_to_sourcing_trip(db, trip_id, observation_id)
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{trip_id}/observations/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_trip_observation(trip_id: UUID, observation_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_observation_from_sourcing_trip(db, trip_id, observation_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sourcing trip {trip_id} is not linked to observation {observation_id}")
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{trip_id}/decisions", response_model=list[DecisionRead])
def list_trip_decisions(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return [DecisionRead.model_validate(d) for d in assoc_service.get_decisions_for_sourcing_trip(db, trip_id)]
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{trip_id}/decisions/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_trip_decision(trip_id: UUID, decision_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_decision_to_sourcing_trip(db, trip_id, decision_id)
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{trip_id}/decisions/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_trip_decision(trip_id: UUID, decision_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_decision_from_sourcing_trip(db, trip_id, decision_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sourcing trip {trip_id} is not linked to decision {decision_id}")
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{trip_id}/purchase-orders", response_model=list[PurchaseOrderRead])
def list_trip_purchase_orders(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return [assoc_service.po_to_read(db, po) for po in assoc_service.get_purchase_orders_for_sourcing_trip(db, trip_id)]
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{trip_id}/purchase-orders/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_trip_purchase_order(trip_id: UUID, purchase_order_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_purchase_order_to_sourcing_trip(db, trip_id, purchase_order_id)
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{trip_id}/purchase-orders/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_trip_purchase_order(trip_id: UUID, purchase_order_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_purchase_order_from_sourcing_trip(db, trip_id, purchase_order_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sourcing trip {trip_id} is not linked to purchase order {purchase_order_id}")
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{trip_id}/inbound-shipments", response_model=list[InboundShipmentRead])
def list_trip_inbound_shipments(trip_id: UUID, db: Session = Depends(get_db)):
    try:
        return [assoc_service.shipment_to_read(db, s) for s in assoc_service.get_inbound_shipments_for_sourcing_trip(db, trip_id)]
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{trip_id}/inbound-shipments/{inbound_shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_trip_inbound_shipment(trip_id: UUID, inbound_shipment_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_inbound_shipment_to_sourcing_trip(db, trip_id, inbound_shipment_id)
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{trip_id}/inbound-shipments/{inbound_shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_trip_inbound_shipment(trip_id: UUID, inbound_shipment_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_inbound_shipment_from_sourcing_trip(db, trip_id, inbound_shipment_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sourcing trip {trip_id} is not linked to inbound shipment {inbound_shipment_id}")
        db.commit()
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
