from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import (
    brand_decisions,
    brand_inbound_shipments,
    brand_initiatives,
    brand_inventory_locations,
    brand_items,
    brand_observations,
    brand_partners,
    brand_purchase_orders,
    brand_sourcing_trips,
)
from app.models.brand import Brand
from app.models.decision import Decision
from app.models.inbound_shipment import InboundShipment
from app.models.initiative import Initiative
from app.models.inventory_location import InventoryLocation
from app.models.item import Item
from app.models.observation import Observation
from app.models.partner import Partner
from app.models.purchase_order import PurchaseOrder
from app.models.sourcing_trip import SourcingTrip
from app.repositories import brand as brand_repo
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
from app.services.purchase_order import _to_read as po_to_read


class BrandNotFoundError(Exception):
    pass


class InitiativeNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class PartnerNotFoundError(Exception):
    pass


class SourcingTripNotFoundError(Exception):
    pass


class ObservationNotFoundError(Exception):
    pass


class DecisionNotFoundError(Exception):
    pass


class PurchaseOrderNotFoundError(Exception):
    pass


class InboundShipmentNotFoundError(Exception):
    pass


class InventoryLocationNotFoundError(Exception):
    pass


class AlreadyLinkedError(Exception):
    pass


class NotLinkedError(Exception):
    pass


def _get_brand_or_raise(db: Session, brand_id: UUID) -> Brand:
    brand = brand_repo.get(db, brand_id)
    if brand is None:
        raise BrandNotFoundError(f"No brand found with ID {brand_id}")
    return brand


def _get_item_or_raise(db: Session, item_id: UUID) -> Item:
    item = item_repo.get(db, item_id)
    if item is None:
        raise ItemNotFoundError(f"No item found with ID {item_id}")
    return item


def _get_partner_or_raise(db: Session, partner_id: UUID) -> Partner:
    partner = partner_repo.get(db, partner_id)
    if partner is None:
        raise PartnerNotFoundError(f"No partner found with ID {partner_id}")
    return partner


def _get_initiative_or_raise(db: Session, initiative_id: UUID) -> Initiative:
    initiative = initiative_repo.get(db, initiative_id)
    if initiative is None:
        raise InitiativeNotFoundError(
            f"No initiative found with ID {initiative_id}"
        )
    return initiative


def _get_sourcing_trip_or_raise(db: Session, trip_id: UUID) -> SourcingTrip:
    trip = trip_repo.get(db, trip_id)
    if trip is None:
        raise SourcingTripNotFoundError(f"No trip found with ID {trip_id}")
    return trip


def _get_observation_or_raise(db: Session, observation_id: UUID) -> Observation:
    observation = observation_repo.get(db, observation_id)
    if observation is None:
        raise ObservationNotFoundError(
            f"No observation found with ID {observation_id}"
        )
    return observation


def _get_decision_or_raise(db: Session, decision_id: UUID) -> Decision:
    decision = decision_repo.get(db, decision_id)
    if decision is None:
        raise DecisionNotFoundError(f"No decision found with ID {decision_id}")
    return decision


def _get_purchase_order_or_raise(db: Session, po_id: UUID) -> PurchaseOrder:
    po = po_repo.get(db, po_id)
    if po is None:
        raise PurchaseOrderNotFoundError(
            f"No purchase order found with ID {po_id}"
        )
    return po


def _get_inbound_shipment_or_raise(
    db: Session, shipment_id: UUID
) -> InboundShipment:
    shipment = shipment_repo.get(db, shipment_id)
    if shipment is None:
        raise InboundShipmentNotFoundError(
            f"No inbound shipment found with ID {shipment_id}"
        )
    return shipment


def _get_inventory_location_or_raise(
    db: Session, location_id: UUID
) -> InventoryLocation:
    location = location_repo.get(db, location_id)
    if location is None:
        raise InventoryLocationNotFoundError(
            f"No inventory location found with ID {location_id}"
        )
    return location


def get_initiatives_for_brand(db: Session, brand_id: UUID) -> list[Initiative]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(Initiative)
            .join(brand_initiatives, brand_initiatives.c.initiative_id == Initiative.id)
            .where(brand_initiatives.c.brand_id == brand_id)
        )
    )


def link_initiative_to_brand(db: Session, brand_id: UUID, initiative_id: UUID) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_initiative_or_raise(db, initiative_id)
    try:
        db.execute(
            brand_initiatives.insert().values(
                brand_id=brand_id,
                initiative_id=initiative_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to initiative {initiative_id}"
        ) from exc


def unlink_initiative_from_brand(
    db: Session, brand_id: UUID, initiative_id: UUID
) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_initiatives).where(
            brand_initiatives.c.brand_id == brand_id,
            brand_initiatives.c.initiative_id == initiative_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_items_for_brand(db: Session, brand_id: UUID) -> list[Item]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(Item)
            .join(brand_items, brand_items.c.item_id == Item.id)
            .where(brand_items.c.brand_id == brand_id)
        )
    )


def link_item_to_brand(db: Session, brand_id: UUID, item_id: UUID) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_item_or_raise(db, item_id)
    try:
        db.execute(
            brand_items.insert().values(
                brand_id=brand_id,
                item_id=item_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to item {item_id}"
        ) from exc


def unlink_item_from_brand(db: Session, brand_id: UUID, item_id: UUID) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_items).where(
            brand_items.c.brand_id == brand_id,
            brand_items.c.item_id == item_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_partners_for_brand(db: Session, brand_id: UUID) -> list[Partner]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(Partner)
            .join(brand_partners, brand_partners.c.partner_id == Partner.id)
            .where(brand_partners.c.brand_id == brand_id)
        )
    )


def link_partner_to_brand(db: Session, brand_id: UUID, partner_id: UUID) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_partner_or_raise(db, partner_id)
    try:
        db.execute(
            brand_partners.insert().values(
                brand_id=brand_id,
                partner_id=partner_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to partner {partner_id}"
        ) from exc


def unlink_partner_from_brand(db: Session, brand_id: UUID, partner_id: UUID) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_partners).where(
            brand_partners.c.brand_id == brand_id,
            brand_partners.c.partner_id == partner_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_sourcing_trips_for_brand(db: Session, brand_id: UUID) -> list[SourcingTrip]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(SourcingTrip)
            .join(
                brand_sourcing_trips,
                brand_sourcing_trips.c.sourcing_trip_id == SourcingTrip.id,
            )
            .where(brand_sourcing_trips.c.brand_id == brand_id)
        )
    )


def link_sourcing_trip_to_brand(
    db: Session, brand_id: UUID, sourcing_trip_id: UUID
) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_sourcing_trip_or_raise(db, sourcing_trip_id)
    try:
        db.execute(
            brand_sourcing_trips.insert().values(
                brand_id=brand_id,
                sourcing_trip_id=sourcing_trip_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to sourcing trip {sourcing_trip_id}"
        ) from exc


def unlink_sourcing_trip_from_brand(
    db: Session, brand_id: UUID, sourcing_trip_id: UUID
) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_sourcing_trips).where(
            brand_sourcing_trips.c.brand_id == brand_id,
            brand_sourcing_trips.c.sourcing_trip_id == sourcing_trip_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_observations_for_brand(db: Session, brand_id: UUID) -> list[Observation]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(Observation)
            .join(brand_observations, brand_observations.c.observation_id == Observation.id)
            .where(brand_observations.c.brand_id == brand_id)
        )
    )


def link_observation_to_brand(db: Session, brand_id: UUID, observation_id: UUID) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_observation_or_raise(db, observation_id)
    try:
        db.execute(
            brand_observations.insert().values(
                brand_id=brand_id,
                observation_id=observation_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to observation {observation_id}"
        ) from exc


def unlink_observation_from_brand(
    db: Session, brand_id: UUID, observation_id: UUID
) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_observations).where(
            brand_observations.c.brand_id == brand_id,
            brand_observations.c.observation_id == observation_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_decisions_for_brand(db: Session, brand_id: UUID) -> list[Decision]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(Decision)
            .join(brand_decisions, brand_decisions.c.decision_id == Decision.id)
            .where(brand_decisions.c.brand_id == brand_id)
        )
    )


def link_decision_to_brand(db: Session, brand_id: UUID, decision_id: UUID) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_decision_or_raise(db, decision_id)
    try:
        db.execute(
            brand_decisions.insert().values(
                brand_id=brand_id,
                decision_id=decision_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to decision {decision_id}"
        ) from exc


def unlink_decision_from_brand(db: Session, brand_id: UUID, decision_id: UUID) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_decisions).where(
            brand_decisions.c.brand_id == brand_id,
            brand_decisions.c.decision_id == decision_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_purchase_orders_for_brand(
    db: Session, brand_id: UUID
) -> list[PurchaseOrder]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(PurchaseOrder)
            .join(
                brand_purchase_orders,
                brand_purchase_orders.c.purchase_order_id == PurchaseOrder.id,
            )
            .where(brand_purchase_orders.c.brand_id == brand_id)
        )
    )


def link_purchase_order_to_brand(
    db: Session, brand_id: UUID, purchase_order_id: UUID
) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_purchase_order_or_raise(db, purchase_order_id)
    try:
        db.execute(
            brand_purchase_orders.insert().values(
                brand_id=brand_id,
                purchase_order_id=purchase_order_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to purchase order {purchase_order_id}"
        ) from exc


def unlink_purchase_order_from_brand(
    db: Session, brand_id: UUID, purchase_order_id: UUID
) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_purchase_orders).where(
            brand_purchase_orders.c.brand_id == brand_id,
            brand_purchase_orders.c.purchase_order_id == purchase_order_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_inbound_shipments_for_brand(
    db: Session, brand_id: UUID
) -> list[InboundShipment]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(InboundShipment)
            .join(
                brand_inbound_shipments,
                brand_inbound_shipments.c.inbound_shipment_id == InboundShipment.id,
            )
            .where(brand_inbound_shipments.c.brand_id == brand_id)
        )
    )


def link_inbound_shipment_to_brand(
    db: Session, brand_id: UUID, inbound_shipment_id: UUID
) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_inbound_shipment_or_raise(db, inbound_shipment_id)
    try:
        db.execute(
            brand_inbound_shipments.insert().values(
                brand_id=brand_id,
                inbound_shipment_id=inbound_shipment_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to inbound shipment {inbound_shipment_id}"
        ) from exc


def unlink_inbound_shipment_from_brand(
    db: Session, brand_id: UUID, inbound_shipment_id: UUID
) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_inbound_shipments).where(
            brand_inbound_shipments.c.brand_id == brand_id,
            brand_inbound_shipments.c.inbound_shipment_id == inbound_shipment_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def get_inventory_locations_for_brand(
    db: Session, brand_id: UUID
) -> list[InventoryLocation]:
    _get_brand_or_raise(db, brand_id)
    return list(
        db.scalars(
            select(InventoryLocation)
            .join(
                brand_inventory_locations,
                brand_inventory_locations.c.inventory_location_id == InventoryLocation.id,
            )
            .where(brand_inventory_locations.c.brand_id == brand_id)
        )
    )


def link_inventory_location_to_brand(
    db: Session, brand_id: UUID, inventory_location_id: UUID
) -> None:
    _get_brand_or_raise(db, brand_id)
    _get_inventory_location_or_raise(db, inventory_location_id)
    try:
        db.execute(
            brand_inventory_locations.insert().values(
                brand_id=brand_id,
                inventory_location_id=inventory_location_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Brand {brand_id} is already linked to inventory location {inventory_location_id}"
        ) from exc


def unlink_inventory_location_from_brand(
    db: Session, brand_id: UUID, inventory_location_id: UUID
) -> bool:
    _get_brand_or_raise(db, brand_id)
    result = db.execute(
        delete(brand_inventory_locations).where(
            brand_inventory_locations.c.brand_id == brand_id,
            brand_inventory_locations.c.inventory_location_id == inventory_location_id,
        )
    )
    db.flush()
    return result.rowcount > 0


def list_brand_association_endpoints(db: Session, brand_id: UUID) -> dict[str, list]:
    return {
        "initiatives": [InitiativeRead.model_validate(i) for i in get_initiatives_for_brand(db, brand_id)],
        "items": [ItemRead.model_validate(i) for i in get_items_for_brand(db, brand_id)],
        "partners": [PartnerRead.model_validate(p) for p in get_partners_for_brand(db, brand_id)],
        "sourcing_trips": [SourcingTripRead.model_validate(t) for t in get_sourcing_trips_for_brand(db, brand_id)],
        "observations": [ObservationRead.model_validate(o) for o in get_observations_for_brand(db, brand_id)],
        "decisions": [DecisionRead.model_validate(d) for d in get_decisions_for_brand(db, brand_id)],
        "purchase_orders": [po_to_read(db, po) for po in get_purchase_orders_for_brand(db, brand_id)],
        "inbound_shipments": [shipment_to_read(db, s) for s in get_inbound_shipments_for_brand(db, brand_id)],
        "inventory_locations": [InventoryLocationRead.model_validate(l) for l in get_inventory_locations_for_brand(db, brand_id)],
    }
