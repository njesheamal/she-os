from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import (
    sourcing_trip_decisions,
    sourcing_trip_inbound_shipments,
    sourcing_trip_items,
    sourcing_trip_observations,
    sourcing_trip_partners,
    sourcing_trip_purchase_orders,
)
from app.models.decision import Decision
from app.models.inbound_shipment import InboundShipment
from app.models.item import Item
from app.models.observation import Observation
from app.models.partner import Partner
from app.models.purchase_order import PurchaseOrder
from app.models.sourcing_trip import SourcingTrip
from app.repositories import decision as decision_repo
from app.repositories import inbound_shipment as shipment_repo
from app.repositories import item as item_repo
from app.repositories import observation as observation_repo
from app.repositories import partner as partner_repo
from app.repositories import purchase_order as po_repo
from app.repositories import sourcing_trip as trip_repo
from app.schemas.decision import DecisionRead
from app.schemas.inbound_shipment import InboundShipmentRead
from app.schemas.item import ItemRead
from app.schemas.observation import ObservationRead
from app.schemas.partner import PartnerRead
from app.schemas.purchase_order import PurchaseOrderRead
from app.services.inbound_shipment import _to_read as shipment_to_read
from app.services.purchase_order import _to_read as po_to_read
from app.services.sourcing_trip import SourcingTripNotFoundError


class AlreadyLinkedError(Exception):
    pass


class NotLinkedError(Exception):
    pass


def _get_trip_or_raise(db: Session, trip_id: UUID) -> SourcingTrip:
    trip = trip_repo.get(db, trip_id)
    if trip is None:
        raise SourcingTripNotFoundError(f"No sourcing trip found with ID {trip_id}")
    return trip


def get_items_for_sourcing_trip(db: Session, trip_id: UUID) -> list[Item]:
    _get_trip_or_raise(db, trip_id)
    return list(
        db.scalars(
            select(Item)
            .join(sourcing_trip_items, sourcing_trip_items.c.item_id == Item.id)
            .where(sourcing_trip_items.c.sourcing_trip_id == trip_id)
        )
    )


def link_item_to_sourcing_trip(db: Session, trip_id: UUID, item_id: UUID) -> None:
    _get_trip_or_raise(db, trip_id)
    item = item_repo.get(db, item_id)
    if item is None:
        raise ValueError(f"No item found with ID {item_id}")
    try:
        db.execute(
            sourcing_trip_items.insert().values(sourcing_trip_id=trip_id, item_id=item_id)
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Sourcing trip {trip_id} is already linked to item {item_id}"
        ) from exc


def unlink_item_from_sourcing_trip(db: Session, trip_id: UUID, item_id: UUID) -> bool:
    _get_trip_or_raise(db, trip_id)
    result = db.execute(
        delete(sourcing_trip_items).where(
            sourcing_trip_items.c.sourcing_trip_id == trip_id,
            sourcing_trip_items.c.item_id == item_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Sourcing trip {trip_id} is not linked to item {item_id}"
        )
    return True


def get_partners_for_sourcing_trip(db: Session, trip_id: UUID) -> list[Partner]:
    _get_trip_or_raise(db, trip_id)
    return list(
        db.scalars(
            select(Partner)
            .join(sourcing_trip_partners, sourcing_trip_partners.c.partner_id == Partner.id)
            .where(sourcing_trip_partners.c.sourcing_trip_id == trip_id)
        )
    )


def link_partner_to_sourcing_trip(
    db: Session, trip_id: UUID, partner_id: UUID
) -> None:
    _get_trip_or_raise(db, trip_id)
    partner = partner_repo.get(db, partner_id)
    if partner is None:
        raise ValueError(f"No partner found with ID {partner_id}")
    try:
        db.execute(
            sourcing_trip_partners.insert().values(
                sourcing_trip_id=trip_id,
                partner_id=partner_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Sourcing trip {trip_id} is already linked to partner {partner_id}"
        ) from exc


def unlink_partner_from_sourcing_trip(
    db: Session, trip_id: UUID, partner_id: UUID
) -> bool:
    _get_trip_or_raise(db, trip_id)
    result = db.execute(
        delete(sourcing_trip_partners).where(
            sourcing_trip_partners.c.sourcing_trip_id == trip_id,
            sourcing_trip_partners.c.partner_id == partner_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Sourcing trip {trip_id} is not linked to partner {partner_id}"
        )
    return True


def get_observations_for_sourcing_trip(
    db: Session, trip_id: UUID
) -> list[Observation]:
    _get_trip_or_raise(db, trip_id)
    return list(
        db.scalars(
            select(Observation)
            .join(
                sourcing_trip_observations,
                sourcing_trip_observations.c.observation_id == Observation.id,
            )
            .where(sourcing_trip_observations.c.sourcing_trip_id == trip_id)
        )
    )


def link_observation_to_sourcing_trip(
    db: Session, trip_id: UUID, observation_id: UUID
) -> None:
    _get_trip_or_raise(db, trip_id)
    observation = observation_repo.get(db, observation_id)
    if observation is None:
        raise ValueError(f"No observation found with ID {observation_id}")
    try:
        db.execute(
            sourcing_trip_observations.insert().values(
                sourcing_trip_id=trip_id,
                observation_id=observation_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Sourcing trip {trip_id} is already linked to observation {observation_id}"
        ) from exc


def unlink_observation_from_sourcing_trip(
    db: Session, trip_id: UUID, observation_id: UUID
) -> bool:
    _get_trip_or_raise(db, trip_id)
    result = db.execute(
        delete(sourcing_trip_observations).where(
            sourcing_trip_observations.c.sourcing_trip_id == trip_id,
            sourcing_trip_observations.c.observation_id == observation_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Sourcing trip {trip_id} is not linked to observation {observation_id}"
        )
    return True


def get_decisions_for_sourcing_trip(db: Session, trip_id: UUID) -> list[Decision]:
    _get_trip_or_raise(db, trip_id)
    return list(
        db.scalars(
            select(Decision)
            .join(sourcing_trip_decisions, sourcing_trip_decisions.c.decision_id == Decision.id)
            .where(sourcing_trip_decisions.c.sourcing_trip_id == trip_id)
        )
    )


def link_decision_to_sourcing_trip(
    db: Session, trip_id: UUID, decision_id: UUID
) -> None:
    _get_trip_or_raise(db, trip_id)
    decision = decision_repo.get(db, decision_id)
    if decision is None:
        raise ValueError(f"No decision found with ID {decision_id}")
    try:
        db.execute(
            sourcing_trip_decisions.insert().values(
                sourcing_trip_id=trip_id,
                decision_id=decision_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Sourcing trip {trip_id} is already linked to decision {decision_id}"
        ) from exc


def unlink_decision_from_sourcing_trip(
    db: Session, trip_id: UUID, decision_id: UUID
) -> bool:
    _get_trip_or_raise(db, trip_id)
    result = db.execute(
        delete(sourcing_trip_decisions).where(
            sourcing_trip_decisions.c.sourcing_trip_id == trip_id,
            sourcing_trip_decisions.c.decision_id == decision_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Sourcing trip {trip_id} is not linked to decision {decision_id}"
        )
    return True


def get_purchase_orders_for_sourcing_trip(
    db: Session, trip_id: UUID
) -> list[PurchaseOrder]:
    _get_trip_or_raise(db, trip_id)
    return list(
        db.scalars(
            select(PurchaseOrder)
            .join(
                sourcing_trip_purchase_orders,
                sourcing_trip_purchase_orders.c.purchase_order_id == PurchaseOrder.id,
            )
            .where(sourcing_trip_purchase_orders.c.sourcing_trip_id == trip_id)
        )
    )


def link_purchase_order_to_sourcing_trip(
    db: Session, trip_id: UUID, purchase_order_id: UUID
) -> None:
    _get_trip_or_raise(db, trip_id)
    po = po_repo.get(db, purchase_order_id)
    if po is None:
        raise ValueError(f"No purchase order found with ID {purchase_order_id}")
    try:
        db.execute(
            sourcing_trip_purchase_orders.insert().values(
                sourcing_trip_id=trip_id,
                purchase_order_id=purchase_order_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Sourcing trip {trip_id} is already linked to purchase order {purchase_order_id}"
        ) from exc


def unlink_purchase_order_from_sourcing_trip(
    db: Session, trip_id: UUID, purchase_order_id: UUID
) -> bool:
    _get_trip_or_raise(db, trip_id)
    result = db.execute(
        delete(sourcing_trip_purchase_orders).where(
            sourcing_trip_purchase_orders.c.sourcing_trip_id == trip_id,
            sourcing_trip_purchase_orders.c.purchase_order_id == purchase_order_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Sourcing trip {trip_id} is not linked to purchase order {purchase_order_id}"
        )
    return True


def get_inbound_shipments_for_sourcing_trip(
    db: Session, trip_id: UUID
) -> list[InboundShipment]:
    _get_trip_or_raise(db, trip_id)
    return list(
        db.scalars(
            select(InboundShipment)
            .join(
                sourcing_trip_inbound_shipments,
                sourcing_trip_inbound_shipments.c.inbound_shipment_id == InboundShipment.id,
            )
            .where(sourcing_trip_inbound_shipments.c.sourcing_trip_id == trip_id)
        )
    )


def link_inbound_shipment_to_sourcing_trip(
    db: Session, trip_id: UUID, inbound_shipment_id: UUID
) -> None:
    _get_trip_or_raise(db, trip_id)
    shipment = shipment_repo.get(db, inbound_shipment_id)
    if shipment is None:
        raise ValueError(f"No inbound shipment found with ID {inbound_shipment_id}")
    try:
        db.execute(
            sourcing_trip_inbound_shipments.insert().values(
                sourcing_trip_id=trip_id,
                inbound_shipment_id=inbound_shipment_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Sourcing trip {trip_id} is already linked to inbound shipment {inbound_shipment_id}"
        ) from exc


def unlink_inbound_shipment_from_sourcing_trip(
    db: Session, trip_id: UUID, inbound_shipment_id: UUID
) -> bool:
    _get_trip_or_raise(db, trip_id)
    result = db.execute(
        delete(sourcing_trip_inbound_shipments).where(
            sourcing_trip_inbound_shipments.c.sourcing_trip_id == trip_id,
            sourcing_trip_inbound_shipments.c.inbound_shipment_id == inbound_shipment_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Sourcing trip {trip_id} is not linked to inbound shipment {inbound_shipment_id}"
        )
    return True
