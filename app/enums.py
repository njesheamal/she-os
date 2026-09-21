# app/enums.py
from enum import StrEnum


class BrandStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class ItemStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"

class PartnerStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class InitiativeStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class SourcingTripStatus(StrEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class DecisionStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_EFFECT = "in_effect"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"

class PurchaseOrderStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    IN_PRODUCTION = "in_production"
    PARTIALLY_FULFILLED = "partially_fulfilled"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"

class InboundShipmentStatus(StrEnum):
    PREPARING = "preparing"
    IN_TRANSIT = "in_transit"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CLOSED = "closed"

class InventoryLocationStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
