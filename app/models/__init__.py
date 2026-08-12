"""Model registry.

Importing this package imports every model and association table, which
registers all of them on ``Base.metadata``. Anything that inspects the
schema — ``create_all``, Alembic autogenerate — must import this package
first, or it will only see the tables that happen to have been imported
elsewhere.
"""

from app.models.brand import Brand
from app.database.lookups import (
    ItemType,
    PartnerType,
    InitiativeType,
    InventoryLocationType,
    InventoryMovementType,
    UnitOfMeasure,
)
from app.models.item import Item
from app.models.partner import Partner
from app.models.initiative import Initiative
from app.models.sourcing_trip import SourcingTrip
from app.models.observation import Observation
from app.models.decision import Decision
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_line import PurchaseOrderLine
from app.models.inbound_shipment import InboundShipment
from app.models.inbound_shipment_line import InboundShipmentLine
from app.models.inventory_location import InventoryLocation
from app.models.inventory_movement import InventoryMovement
from app.models.inventory_balance import InventoryBalance
from app.models import associations  # noqa: F401  (Table objects, no class to import)

__all__ = [
    "Brand",
    "ItemType",
    "PartnerType",
    "InitiativeType",
    "InventoryLocationType",
    "InventoryMovementType",
    "UnitOfMeasure",
    "Item",
    "Partner",
    "Initiative",
    "SourcingTrip",
    "Observation",
    "Decision",
    "PurchaseOrder",
    "PurchaseOrderLine",
    "InboundShipment",
    "InboundShipmentLine",
    "InventoryLocation",
    "InventoryMovement",
    "InventoryBalance",
]
