from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import (
    initiative_decisions,
    initiative_inbound_shipments,
    initiative_inventory_locations,
    initiative_items,
    initiative_observations,
    initiative_partners,
    initiative_purchase_orders,
    initiative_sourcing_trips,
)
from app.models.decision import Decision
from app.models.inbound_shipment import InboundShipment
from app.models.initiative import Initiative
from app.models.inventory_location import InventoryLocation
from app.models.item import Item
from app.models.observation import Observation
from app.models.partner import Partner
from app.models.purchase_order import PurchaseOrder
from app.models.sourcing_trip import SourcingTrip
from app.repositories import decision as decision_repo
from app.repositories import inbound_shipment as shipment_repo
from app.repositories import initiative as initiative_repo
from app.repositories import inventory_location as location_repo
from app.repositories import item as item_repo
from app.repositories import observation as observation_repo
from app.repositories import partner as partner_repo
from app.repositories import purchase_order as po_repo
from app.repositories import sourcing_trip as trip_repo
from app.schemas.decision import DecisionRead
from app.schemas.inbound_shipment import InboundShipmentRead
from app.schemas.initiative import InitiativeRead
from app.schemas.inventory_location import InventoryLocationRead
from app.schemas.item import ItemRead
from app.schemas.observation import ObservationRead
from app.schemas.partner import PartnerRead
from app.schemas.purchase_order import PurchaseOrderRead
from app.schemas.sourcing_trip import SourcingTripRead
from app.services.inbound_shipment import _to_read as shipment_to_read
from app.services.initiative import InitiativeNotFoundError
from app.services.item import ItemNotFoundError
from app.services.partner import PartnerNotFoundError
from app.services.purchase_order import _to_read as po_to_read


class AlreadyLinkedError(Exception):
    pass


class NotLinkedError(Exception):
    pass


def _get_initiative_or_raise(db: Session, initiative_id: UUID) -> Initiative:
    initiative = initiative_repo.get(db, initiative_id)
    if initiative is None:
        raise InitiativeNotFoundError(
            f"No initiative found with ID {initiative_id}"
        )
    return initiative


def get_items_for_initiative(db: Session, initiative_id: UUID) -> list[Item]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(Item)
            .join(initiative_items, initiative_items.c.item_id == Item.id)
            .where(initiative_items.c.initiative_id == initiative_id)
        )
    )


def link_item_to_initiative(db: Session, initiative_id: UUID, item_id: UUID) -> None:
    _get_initiative_or_raise(db, initiative_id)
    item = item_repo.get(db, item_id)
    if item is None:
        raise ItemNotFoundError(f"No item found with ID {item_id}")
    try:
        db.execute(
            initiative_items.insert().values(
                initiative_id=initiative_id,
                item_id=item_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to item {item_id}"
        ) from exc


def unlink_item_from_initiative(
    db: Session, initiative_id: UUID, item_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_items).where(
            initiative_items.c.initiative_id == initiative_id,
            initiative_items.c.item_id == item_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to item {item_id}"
        )
    return True


def get_partners_for_initiative(db: Session, initiative_id: UUID) -> list[Partner]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(Partner)
            .join(initiative_partners, initiative_partners.c.partner_id == Partner.id)
            .where(initiative_partners.c.initiative_id == initiative_id)
        )
    )


def link_partner_to_initiative(
    db: Session, initiative_id: UUID, partner_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    partner = partner_repo.get(db, partner_id)
    if partner is None:
        raise PartnerNotFoundError(f"No partner found with ID {partner_id}")
    try:
        db.execute(
            initiative_partners.insert().values(
                initiative_id=initiative_id,
                partner_id=partner_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to partner {partner_id}"
        ) from exc


def unlink_partner_from_initiative(
    db: Session, initiative_id: UUID, partner_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_partners).where(
            initiative_partners.c.initiative_id == initiative_id,
            initiative_partners.c.partner_id == partner_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to partner {partner_id}"
        )
    return True


def get_sourcing_trips_for_initiative(
    db: Session, initiative_id: UUID
) -> list[SourcingTrip]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(SourcingTrip)
            .join(
                initiative_sourcing_trips,
                initiative_sourcing_trips.c.sourcing_trip_id == SourcingTrip.id,
            )
            .where(initiative_sourcing_trips.c.initiative_id == initiative_id)
        )
    )


def link_sourcing_trip_to_initiative(
    db: Session, initiative_id: UUID, sourcing_trip_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    trip = trip_repo.get(db, sourcing_trip_id)
    if trip is None:
        raise ValueError(f"No sourcing trip found with ID {sourcing_trip_id}")
    try:
        db.execute(
            initiative_sourcing_trips.insert().values(
                initiative_id=initiative_id,
                sourcing_trip_id=sourcing_trip_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to sourcing trip {sourcing_trip_id}"
        ) from exc


def unlink_sourcing_trip_from_initiative(
    db: Session, initiative_id: UUID, sourcing_trip_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_sourcing_trips).where(
            initiative_sourcing_trips.c.initiative_id == initiative_id,
            initiative_sourcing_trips.c.sourcing_trip_id == sourcing_trip_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to sourcing trip {sourcing_trip_id}"
        )
    return True


def get_observations_for_initiative(
    db: Session, initiative_id: UUID
) -> list[Observation]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(Observation)
            .join(
                initiative_observations,
                initiative_observations.c.observation_id == Observation.id,
            )
            .where(initiative_observations.c.initiative_id == initiative_id)
        )
    )


def link_observation_to_initiative(
    db: Session, initiative_id: UUID, observation_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    observation = observation_repo.get(db, observation_id)
    if observation is None:
        raise ValueError(f"No observation found with ID {observation_id}")
    try:
        db.execute(
            initiative_observations.insert().values(
                initiative_id=initiative_id,
                observation_id=observation_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to observation {observation_id}"
        ) from exc


def unlink_observation_from_initiative(
    db: Session, initiative_id: UUID, observation_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_observations).where(
            initiative_observations.c.initiative_id == initiative_id,
            initiative_observations.c.observation_id == observation_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to observation {observation_id}"
        )
    return True


def get_decisions_for_initiative(db: Session, initiative_id: UUID) -> list[Decision]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(Decision)
            .join(initiative_decisions, initiative_decisions.c.decision_id == Decision.id)
            .where(initiative_decisions.c.initiative_id == initiative_id)
        )
    )


def link_decision_to_initiative(
    db: Session, initiative_id: UUID, decision_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    decision = decision_repo.get(db, decision_id)
    if decision is None:
        raise ValueError(f"No decision found with ID {decision_id}")
    try:
        db.execute(
            initiative_decisions.insert().values(
                initiative_id=initiative_id,
                decision_id=decision_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to decision {decision_id}"
        ) from exc


def unlink_decision_from_initiative(
    db: Session, initiative_id: UUID, decision_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_decisions).where(
            initiative_decisions.c.initiative_id == initiative_id,
            initiative_decisions.c.decision_id == decision_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to decision {decision_id}"
        )
    return True


def get_purchase_orders_for_initiative(
    db: Session, initiative_id: UUID
) -> list[PurchaseOrder]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(PurchaseOrder)
            .join(
                initiative_purchase_orders,
                initiative_purchase_orders.c.purchase_order_id == PurchaseOrder.id,
            )
            .where(initiative_purchase_orders.c.initiative_id == initiative_id)
        )
    )


def link_purchase_order_to_initiative(
    db: Session, initiative_id: UUID, purchase_order_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    po = po_repo.get(db, purchase_order_id)
    if po is None:
        raise ValueError(f"No purchase order found with ID {purchase_order_id}")
    try:
        db.execute(
            initiative_purchase_orders.insert().values(
                initiative_id=initiative_id,
                purchase_order_id=purchase_order_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to purchase order {purchase_order_id}"
        ) from exc


def unlink_purchase_order_from_initiative(
    db: Session, initiative_id: UUID, purchase_order_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_purchase_orders).where(
            initiative_purchase_orders.c.initiative_id == initiative_id,
            initiative_purchase_orders.c.purchase_order_id == purchase_order_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to purchase order {purchase_order_id}"
        )
    return True


def get_inbound_shipments_for_initiative(
    db: Session, initiative_id: UUID
) -> list[InboundShipment]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(InboundShipment)
            .join(
                initiative_inbound_shipments,
                initiative_inbound_shipments.c.inbound_shipment_id == InboundShipment.id,
            )
            .where(initiative_inbound_shipments.c.initiative_id == initiative_id)
        )
    )


def link_inbound_shipment_to_initiative(
    db: Session, initiative_id: UUID, inbound_shipment_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    shipment = shipment_repo.get(db, inbound_shipment_id)
    if shipment is None:
        raise ValueError(f"No inbound shipment found with ID {inbound_shipment_id}")
    try:
        db.execute(
            initiative_inbound_shipments.insert().values(
                initiative_id=initiative_id,
                inbound_shipment_id=inbound_shipment_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to inbound shipment {inbound_shipment_id}"
        ) from exc


def unlink_inbound_shipment_from_initiative(
    db: Session, initiative_id: UUID, inbound_shipment_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_inbound_shipments).where(
            initiative_inbound_shipments.c.initiative_id == initiative_id,
            initiative_inbound_shipments.c.inbound_shipment_id == inbound_shipment_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to inbound shipment {inbound_shipment_id}"
        )
    return True


def get_inventory_locations_for_initiative(
    db: Session, initiative_id: UUID
) -> list[InventoryLocation]:
    _get_initiative_or_raise(db, initiative_id)
    return list(
        db.scalars(
            select(InventoryLocation)
            .join(
                initiative_inventory_locations,
                initiative_inventory_locations.c.inventory_location_id == InventoryLocation.id,
            )
            .where(initiative_inventory_locations.c.initiative_id == initiative_id)
        )
    )


def link_inventory_location_to_initiative(
    db: Session, initiative_id: UUID, inventory_location_id: UUID
) -> None:
    _get_initiative_or_raise(db, initiative_id)
    location = location_repo.get(db, inventory_location_id)
    if location is None:
        raise ValueError(f"No inventory location found with ID {inventory_location_id}")
    try:
        db.execute(
            initiative_inventory_locations.insert().values(
                initiative_id=initiative_id,
                inventory_location_id=inventory_location_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Initiative {initiative_id} is already linked to inventory location {inventory_location_id}"
        ) from exc


def unlink_inventory_location_from_initiative(
    db: Session, initiative_id: UUID, inventory_location_id: UUID
) -> bool:
    _get_initiative_or_raise(db, initiative_id)
    result = db.execute(
        delete(initiative_inventory_locations).where(
            initiative_inventory_locations.c.initiative_id == initiative_id,
            initiative_inventory_locations.c.inventory_location_id == inventory_location_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Initiative {initiative_id} is not linked to inventory location {inventory_location_id}"
        )
    return True
