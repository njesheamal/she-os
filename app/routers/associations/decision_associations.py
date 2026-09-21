from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.inbound_shipment import InboundShipmentRead
from app.schemas.inventory_location import InventoryLocationRead
from app.schemas.item import ItemRead
from app.schemas.partner import PartnerRead
from app.schemas.purchase_order import PurchaseOrderRead
from app.services.associations import decision_associations as assoc_service
from app.services.decision import DecisionNotFoundError
from app.services.inbound_shipment import InboundShipmentNotFoundError
from app.services.inventory_location import InventoryLocationNotFoundError
from app.services.item import ItemNotFoundError
from app.services.partner import PartnerNotFoundError
from app.services.purchase_order import PurchaseOrderNotFoundError

router = APIRouter(prefix="/decisions", tags=["decision associations"])


@router.get("/{decision_id}/items", response_model=list[ItemRead])
def list_decision_items(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return [ItemRead.model_validate(i) for i in assoc_service.get_items_for_decision(db, decision_id)]
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{decision_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_decision_item(decision_id: UUID, item_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_item_to_decision(db, decision_id, item_id)
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{decision_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_decision_item(decision_id: UUID, item_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_item_from_decision(db, decision_id, item_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Decision {decision_id} is not linked to item {item_id}")
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{decision_id}/partners", response_model=list[PartnerRead])
def list_decision_partners(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return [PartnerRead.model_validate(p) for p in assoc_service.get_partners_for_decision(db, decision_id)]
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{decision_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_decision_partner(decision_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_partner_to_decision(db, decision_id, partner_id)
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except PartnerNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{decision_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_decision_partner(decision_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_partner_from_decision(db, decision_id, partner_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Decision {decision_id} is not linked to partner {partner_id}")
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{decision_id}/purchase-orders", response_model=list[PurchaseOrderRead])
def list_decision_purchase_orders(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return [assoc_service.po_to_read(db, po) for po in assoc_service.get_purchase_orders_for_decision(db, decision_id)]
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{decision_id}/purchase-orders/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_decision_purchase_order(decision_id: UUID, purchase_order_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_purchase_order_to_decision(db, decision_id, purchase_order_id)
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except PurchaseOrderNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{decision_id}/purchase-orders/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_decision_purchase_order(decision_id: UUID, purchase_order_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_purchase_order_from_decision(db, decision_id, purchase_order_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Decision {decision_id} is not linked to purchase order {purchase_order_id}")
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{decision_id}/inbound-shipments", response_model=list[InboundShipmentRead])
def list_decision_inbound_shipments(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return [assoc_service.shipment_to_read(db, s) for s in assoc_service.get_inbound_shipments_for_decision(db, decision_id)]
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{decision_id}/inbound-shipments/{inbound_shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_decision_inbound_shipment(decision_id: UUID, inbound_shipment_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_inbound_shipment_to_decision(db, decision_id, inbound_shipment_id)
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InboundShipmentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{decision_id}/inbound-shipments/{inbound_shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_decision_inbound_shipment(decision_id: UUID, inbound_shipment_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_inbound_shipment_from_decision(db, decision_id, inbound_shipment_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Decision {decision_id} is not linked to inbound shipment {inbound_shipment_id}")
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{decision_id}/inventory-locations", response_model=list[InventoryLocationRead])
def list_decision_inventory_locations(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return [InventoryLocationRead.model_validate(l) for l in assoc_service.get_inventory_locations_for_decision(db, decision_id)]
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{decision_id}/inventory-locations/{inventory_location_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_decision_inventory_location(decision_id: UUID, inventory_location_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_inventory_location_to_decision(db, decision_id, inventory_location_id)
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except InventoryLocationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{decision_id}/inventory-locations/{inventory_location_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_decision_inventory_location(decision_id: UUID, inventory_location_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_inventory_location_from_decision(db, decision_id, inventory_location_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Decision {decision_id} is not linked to inventory location {inventory_location_id}")
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/{decision_id}/inventory-movements", response_model=list[object])
def list_decision_inventory_movements(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return assoc_service.get_inventory_movements_for_decision(db, decision_id)
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{decision_id}/inventory-movements/{inventory_movement_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_decision_inventory_movement(decision_id: UUID, inventory_movement_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_inventory_movement_to_decision(db, decision_id, inventory_movement_id)
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{decision_id}/inventory-movements/{inventory_movement_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_decision_inventory_movement(decision_id: UUID, inventory_movement_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = assoc_service.unlink_inventory_movement_from_decision(db, decision_id, inventory_movement_id)
        if not deleted:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Decision {decision_id} is not linked to inventory movement {inventory_movement_id}")
        db.commit()
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
