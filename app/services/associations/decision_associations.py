from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import (
    decision_inbound_shipments,
    decision_inventory_locations,
    decision_inventory_movements,
    decision_items,
    decision_partners,
    decision_purchase_orders,
)
from app.models.decision import Decision
from app.models.inbound_shipment import InboundShipment
from app.models.inventory_location import InventoryLocation
from app.models.inventory_movement import InventoryMovement
from app.models.item import Item
from app.models.partner import Partner
from app.models.purchase_order import PurchaseOrder
from app.repositories import decision as decision_repo
from app.repositories import inbound_shipment as shipment_repo
from app.repositories import inventory_location as location_repo
from app.repositories import inventory_movements as movement_repo
from app.repositories import item as item_repo
from app.repositories import partner as partner_repo
from app.repositories import purchase_order as po_repo
from app.services.decision import DecisionNotFoundError
from app.services.inbound_shipment import _to_read as shipment_to_read
from app.services.purchase_order import _to_read as po_to_read


class AlreadyLinkedError(Exception):
    pass


class NotLinkedError(Exception):
    pass


def _get_decision_or_raise(db: Session, decision_id: UUID) -> Decision:
    decision = decision_repo.get(db, decision_id)
    if decision is None:
        raise DecisionNotFoundError(f"No decision found with ID {decision_id}")
    return decision


def get_items_for_decision(db: Session, decision_id: UUID) -> list[Item]:
    _get_decision_or_raise(db, decision_id)
    return list(
        db.scalars(
            select(Item)
            .join(decision_items, decision_items.c.item_id == Item.id)
            .where(decision_items.c.decision_id == decision_id)
        )
    )


def link_item_to_decision(db: Session, decision_id: UUID, item_id: UUID) -> None:
    _get_decision_or_raise(db, decision_id)
    if item_repo.get(db, item_id) is None:
        raise ValueError(f"No item found with ID {item_id}")
    try:
        db.execute(decision_items.insert().values(decision_id=decision_id, item_id=item_id))
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(f"Decision {decision_id} is already linked to item {item_id}") from exc


def unlink_item_from_decision(db: Session, decision_id: UUID, item_id: UUID) -> bool:
    _get_decision_or_raise(db, decision_id)
    result = db.execute(delete(decision_items).where(decision_items.c.decision_id == decision_id, decision_items.c.item_id == item_id))
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(f"Decision {decision_id} is not linked to item {item_id}")
    return True


def get_partners_for_decision(db: Session, decision_id: UUID) -> list[Partner]:
    _get_decision_or_raise(db, decision_id)
    return list(
        db.scalars(
            select(Partner)
            .join(decision_partners, decision_partners.c.partner_id == Partner.id)
            .where(decision_partners.c.decision_id == decision_id)
        )
    )


def link_partner_to_decision(db: Session, decision_id: UUID, partner_id: UUID) -> None:
    _get_decision_or_raise(db, decision_id)
    if partner_repo.get(db, partner_id) is None:
        raise ValueError(f"No partner found with ID {partner_id}")
    try:
        db.execute(decision_partners.insert().values(decision_id=decision_id, partner_id=partner_id))
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(f"Decision {decision_id} is already linked to partner {partner_id}") from exc


def unlink_partner_from_decision(db: Session, decision_id: UUID, partner_id: UUID) -> bool:
    _get_decision_or_raise(db, decision_id)
    result = db.execute(delete(decision_partners).where(decision_partners.c.decision_id == decision_id, decision_partners.c.partner_id == partner_id))
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(f"Decision {decision_id} is not linked to partner {partner_id}")
    return True


def get_purchase_orders_for_decision(db: Session, decision_id: UUID) -> list[PurchaseOrder]:
    _get_decision_or_raise(db, decision_id)
    return list(
        db.scalars(
            select(PurchaseOrder)
            .join(decision_purchase_orders, decision_purchase_orders.c.purchase_order_id == PurchaseOrder.id)
            .where(decision_purchase_orders.c.decision_id == decision_id)
        )
    )


def link_purchase_order_to_decision(db: Session, decision_id: UUID, purchase_order_id: UUID) -> None:
    _get_decision_or_raise(db, decision_id)
    if po_repo.get(db, purchase_order_id) is None:
        raise ValueError(f"No purchase order found with ID {purchase_order_id}")
    try:
        db.execute(decision_purchase_orders.insert().values(decision_id=decision_id, purchase_order_id=purchase_order_id))
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(f"Decision {decision_id} is already linked to purchase order {purchase_order_id}") from exc


def unlink_purchase_order_from_decision(db: Session, decision_id: UUID, purchase_order_id: UUID) -> bool:
    _get_decision_or_raise(db, decision_id)
    result = db.execute(delete(decision_purchase_orders).where(decision_purchase_orders.c.decision_id == decision_id, decision_purchase_orders.c.purchase_order_id == purchase_order_id))
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(f"Decision {decision_id} is not linked to purchase order {purchase_order_id}")
    return True


def get_inbound_shipments_for_decision(db: Session, decision_id: UUID) -> list[InboundShipment]:
    _get_decision_or_raise(db, decision_id)
    return list(
        db.scalars(
            select(InboundShipment)
            .join(decision_inbound_shipments, decision_inbound_shipments.c.inbound_shipment_id == InboundShipment.id)
            .where(decision_inbound_shipments.c.decision_id == decision_id)
        )
    )


def link_inbound_shipment_to_decision(db: Session, decision_id: UUID, inbound_shipment_id: UUID) -> None:
    _get_decision_or_raise(db, decision_id)
    if shipment_repo.get(db, inbound_shipment_id) is None:
        raise ValueError(f"No inbound shipment found with ID {inbound_shipment_id}")
    try:
        db.execute(decision_inbound_shipments.insert().values(decision_id=decision_id, inbound_shipment_id=inbound_shipment_id))
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(f"Decision {decision_id} is already linked to inbound shipment {inbound_shipment_id}") from exc


def unlink_inbound_shipment_from_decision(db: Session, decision_id: UUID, inbound_shipment_id: UUID) -> bool:
    _get_decision_or_raise(db, decision_id)
    result = db.execute(delete(decision_inbound_shipments).where(decision_inbound_shipments.c.decision_id == decision_id, decision_inbound_shipments.c.inbound_shipment_id == inbound_shipment_id))
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(f"Decision {decision_id} is not linked to inbound shipment {inbound_shipment_id}")
    return True


def get_inventory_locations_for_decision(db: Session, decision_id: UUID) -> list[InventoryLocation]:
    _get_decision_or_raise(db, decision_id)
    return list(
        db.scalars(
            select(InventoryLocation)
            .join(decision_inventory_locations, decision_inventory_locations.c.inventory_location_id == InventoryLocation.id)
            .where(decision_inventory_locations.c.decision_id == decision_id)
        )
    )


def link_inventory_location_to_decision(db: Session, decision_id: UUID, inventory_location_id: UUID) -> None:
    _get_decision_or_raise(db, decision_id)
    if location_repo.get(db, inventory_location_id) is None:
        raise ValueError(f"No inventory location found with ID {inventory_location_id}")
    try:
        db.execute(decision_inventory_locations.insert().values(decision_id=decision_id, inventory_location_id=inventory_location_id))
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(f"Decision {decision_id} is already linked to inventory location {inventory_location_id}") from exc


def unlink_inventory_location_from_decision(db: Session, decision_id: UUID, inventory_location_id: UUID) -> bool:
    _get_decision_or_raise(db, decision_id)
    result = db.execute(delete(decision_inventory_locations).where(decision_inventory_locations.c.decision_id == decision_id, decision_inventory_locations.c.inventory_location_id == inventory_location_id))
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(f"Decision {decision_id} is not linked to inventory location {inventory_location_id}")
    return True


def get_inventory_movements_for_decision(db: Session, decision_id: UUID) -> list[InventoryMovement]:
    _get_decision_or_raise(db, decision_id)
    return list(
        db.scalars(
            select(InventoryMovement)
            .join(decision_inventory_movements, decision_inventory_movements.c.inventory_movement_id == InventoryMovement.id)
            .where(decision_inventory_movements.c.decision_id == decision_id)
        )
    )


def link_inventory_movement_to_decision(db: Session, decision_id: UUID, inventory_movement_id: UUID) -> None:
    _get_decision_or_raise(db, decision_id)
    movement = movement_repo.get(db, inventory_movement_id)
    if movement is None:
        raise ValueError(f"No inventory movement found with ID {inventory_movement_id}")
    try:
        db.execute(
            decision_inventory_movements.insert().values(
                decision_id=decision_id,
                inventory_movement_id=inventory_movement_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Decision {decision_id} is already linked to inventory movement {inventory_movement_id}"
        ) from exc


def unlink_inventory_movement_from_decision(db: Session, decision_id: UUID, inventory_movement_id: UUID) -> bool:
    _get_decision_or_raise(db, decision_id)
    result = db.execute(
        delete(decision_inventory_movements).where(
            decision_inventory_movements.c.decision_id == decision_id,
            decision_inventory_movements.c.inventory_movement_id == inventory_movement_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Decision {decision_id} is not linked to inventory movement {inventory_movement_id}"
        )
    return True
