from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import (
    observation_decisions,
    observation_inbound_shipments,
    observation_inventory_locations,
    observation_inventory_movements,
    observation_items,
    observation_partners,
    observation_purchase_orders,
)
from app.models.decision import Decision
from app.models.inbound_shipment import InboundShipment
from app.models.inventory_location import InventoryLocation
from app.models.inventory_movement import InventoryMovement
from app.models.item import Item
from app.models.observation import Observation
from app.models.partner import Partner
from app.models.purchase_order import PurchaseOrder
from app.repositories import decision as decision_repo
from app.repositories import inbound_shipment as shipment_repo
from app.repositories import inventory_location as location_repo
from app.repositories import inventory_movements as movement_repo
from app.repositories import item as item_repo
from app.repositories import observation as observation_repo
from app.repositories import partner as partner_repo
from app.repositories import purchase_order as po_repo
from app.services.observation import ObservationNotFoundError
from app.services.inbound_shipment import _to_read as shipment_to_read
from app.services.purchase_order import _to_read as po_to_read


class AlreadyLinkedError(Exception):
    pass


class NotLinkedError(Exception):
    pass


def _get_observation_or_raise(db: Session, observation_id: UUID) -> Observation:
    observation = observation_repo.get(db, observation_id)
    if observation is None:
        raise ObservationNotFoundError(f"No observation found with ID {observation_id}")
    return observation


def get_decisions_for_observation(db: Session, observation_id: UUID) -> list[Decision]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(Decision)
            .join(observation_decisions, observation_decisions.c.decision_id == Decision.id)
            .where(observation_decisions.c.observation_id == observation_id)
        )
    )


def get_items_for_observation(db: Session, observation_id: UUID) -> list[Item]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(Item)
            .join(observation_items, observation_items.c.item_id == Item.id)
            .where(observation_items.c.observation_id == observation_id)
        )
    )


def get_partners_for_observation(db: Session, observation_id: UUID) -> list[Partner]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(Partner)
            .join(observation_partners, observation_partners.c.partner_id == Partner.id)
            .where(observation_partners.c.observation_id == observation_id)
        )
    )


def get_purchase_orders_for_observation(db: Session, observation_id: UUID) -> list[PurchaseOrder]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(PurchaseOrder)
            .join(observation_purchase_orders, observation_purchase_orders.c.purchase_order_id == PurchaseOrder.id)
            .where(observation_purchase_orders.c.observation_id == observation_id)
        )
    )


def get_inbound_shipments_for_observation(db: Session, observation_id: UUID) -> list[InboundShipment]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(InboundShipment)
            .join(observation_inbound_shipments, observation_inbound_shipments.c.inbound_shipment_id == InboundShipment.id)
            .where(observation_inbound_shipments.c.observation_id == observation_id)
        )
    )


def get_inventory_locations_for_observation(db: Session, observation_id: UUID) -> list[InventoryLocation]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(InventoryLocation)
            .join(observation_inventory_locations, observation_inventory_locations.c.inventory_location_id == InventoryLocation.id)
            .where(observation_inventory_locations.c.observation_id == observation_id)
        )
    )


def get_inventory_movements_for_observation(db: Session, observation_id: UUID) -> list[InventoryMovement]:
    _get_observation_or_raise(db, observation_id)
    return list(
        db.scalars(
            select(InventoryMovement)
            .join(observation_inventory_movements, observation_inventory_movements.c.inventory_movement_id == InventoryMovement.id)
            .where(observation_inventory_movements.c.observation_id == observation_id)
        )
    )


def link_inventory_movement_to_observation(db: Session, observation_id: UUID, inventory_movement_id: UUID) -> None:
    _get_observation_or_raise(db, observation_id)
    movement = movement_repo.get(db, inventory_movement_id)
    if movement is None:
        raise ValueError(f"No inventory movement found with ID {inventory_movement_id}")
    try:
        db.execute(
            observation_inventory_movements.insert().values(
                observation_id=observation_id,
                inventory_movement_id=inventory_movement_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Observation {observation_id} is already linked to inventory movement {inventory_movement_id}"
        ) from exc


def unlink_inventory_movement_from_observation(db: Session, observation_id: UUID, inventory_movement_id: UUID) -> bool:
    _get_observation_or_raise(db, observation_id)
    result = db.execute(
        delete(observation_inventory_movements).where(
            observation_inventory_movements.c.observation_id == observation_id,
            observation_inventory_movements.c.inventory_movement_id == inventory_movement_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Observation {observation_id} is not linked to inventory movement {inventory_movement_id}"
        )
    return True
