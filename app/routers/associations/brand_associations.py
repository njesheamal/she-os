from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.decision import DecisionRead
from app.schemas.inbound_shipment import InboundShipmentRead
from app.schemas.initiative import InitiativeRead
from app.schemas.inventory_location import InventoryLocationRead
from app.schemas.item import ItemRead
from app.schemas.observation import ObservationRead
from app.schemas.partner import PartnerRead
from app.schemas.purchase_order import PurchaseOrderRead
from app.schemas.sourcing_trip import SourcingTripRead
from app.services.associations import brand_associations as assoc_service
from app.services.brand import BrandNotFoundError
from app.services.decision import DecisionNotFoundError
from app.services.inbound_shipment import InboundShipmentNotFoundError
from app.services.initiative import InitiativeNotFoundError
from app.services.inventory_location import InventoryLocationNotFoundError
from app.services.item import ItemNotFoundError
from app.services.observation import ObservationNotFoundError
from app.services.partner import PartnerNotFoundError
from app.services.purchase_order import PurchaseOrderNotFoundError
from app.services.sourcing_trip import SourcingTripNotFoundError

router = APIRouter(prefix="/brands", tags=["brand associations"])


def _brand_error(exc: Exception):
    raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/initiatives", response_model=list[InitiativeRead])
def list_brand_initiatives(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [InitiativeRead.model_validate(i) for i in assoc_service.get_initiatives_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.get("/{brand_id}/items", response_model=list[ItemRead])
def list_brand_items(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [ItemRead.model_validate(i) for i in assoc_service.get_items_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_item(brand_id: UUID, item_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_item_to_brand(db, brand_id, item_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_item(brand_id: UUID, item_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_item_from_brand(db, brand_id, item_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to item {item_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/partners", response_model=list[PartnerRead])
def list_brand_partners(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [PartnerRead.model_validate(p) for p in assoc_service.get_partners_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.get("/{brand_id}/sourcing-trips", response_model=list[SourcingTripRead])
def list_brand_sourcing_trips(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [SourcingTripRead.model_validate(t) for t in assoc_service.get_sourcing_trips_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/initiatives/{initiative_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_initiative(brand_id: UUID, initiative_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_initiative_to_brand(db, brand_id, initiative_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InitiativeNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/initiatives/{initiative_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_initiative(brand_id: UUID, initiative_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_initiative_from_brand(db, brand_id, initiative_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to initiative {initiative_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/observations", response_model=list[ObservationRead])
def list_brand_observations(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [ObservationRead.model_validate(o) for o in assoc_service.get_observations_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_partner(brand_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_partner_to_brand(db, brand_id, partner_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except PartnerNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_partner(brand_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_partner_from_brand(db, brand_id, partner_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to partner {partner_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{brand_id}/sourcing-trips/{sourcing_trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_sourcing_trip(brand_id: UUID, sourcing_trip_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_sourcing_trip_to_brand(db, brand_id, sourcing_trip_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except SourcingTripNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/sourcing-trips/{sourcing_trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_sourcing_trip(brand_id: UUID, sourcing_trip_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_sourcing_trip_from_brand(db, brand_id, sourcing_trip_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to sourcing trip {sourcing_trip_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{brand_id}/observations/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_observation(brand_id: UUID, observation_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_observation_to_brand(db, brand_id, observation_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ObservationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/observations/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_observation(brand_id: UUID, observation_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_observation_from_brand(db, brand_id, observation_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to observation {observation_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/decisions", response_model=list[DecisionRead])
def list_brand_decisions(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [DecisionRead.model_validate(d) for d in assoc_service.get_decisions_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/decisions/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_decision(brand_id: UUID, decision_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_decision_to_brand(db, brand_id, decision_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/decisions/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_decision(brand_id: UUID, decision_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_decision_from_brand(db, brand_id, decision_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to decision {decision_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/purchase-orders", response_model=list[PurchaseOrderRead])
def list_brand_purchase_orders(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [assoc_service.po_to_read(db, po) for po in assoc_service.get_purchase_orders_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/purchase-orders/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_purchase_order(brand_id: UUID, purchase_order_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_purchase_order_to_brand(db, brand_id, purchase_order_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except PurchaseOrderNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/purchase-orders/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_purchase_order(brand_id: UUID, purchase_order_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_purchase_order_from_brand(db, brand_id, purchase_order_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to purchase order {purchase_order_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/inbound-shipments", response_model=list[InboundShipmentRead])
def list_brand_inbound_shipments(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [assoc_service.shipment_to_read(db, s) for s in assoc_service.get_inbound_shipments_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/inbound-shipments/{inbound_shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_inbound_shipment(brand_id: UUID, inbound_shipment_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_inbound_shipment_to_brand(db, brand_id, inbound_shipment_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InboundShipmentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/inbound-shipments/{inbound_shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_inbound_shipment(brand_id: UUID, inbound_shipment_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_inbound_shipment_from_brand(db, brand_id, inbound_shipment_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to inbound shipment {inbound_shipment_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{brand_id}/inventory-locations", response_model=list[InventoryLocationRead])
def list_brand_inventory_locations(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        return [InventoryLocationRead.model_validate(l) for l in assoc_service.get_inventory_locations_for_brand(db, brand_id)]
    except BrandNotFoundError as exc:
        _brand_error(exc)


@router.post("/{brand_id}/inventory-locations/{inventory_location_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_brand_inventory_location(brand_id: UUID, inventory_location_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_inventory_location_to_brand(db, brand_id, inventory_location_id)
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InventoryLocationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}/inventory-locations/{inventory_location_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_brand_inventory_location(brand_id: UUID, inventory_location_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_inventory_location_from_brand(db, brand_id, inventory_location_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brand {brand_id} is not linked to inventory location {inventory_location_id}")
        db.commit()
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
