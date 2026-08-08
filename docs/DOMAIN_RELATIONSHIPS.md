DOMAIN_RELATIONSHIPS.md

Purpose

This document defines the business relationships between core SHÉ OS entities.

The purpose of this document is not to define database implementation.

The purpose is to define how the SHÉ ESTATE ecosystem operates so that future database design reflects real business workflows.

⸻

Core Entities

* Brand
* Initiative
* Item
* Partner
* SourcingTrip
* Observation
* Decision
* PurchaseOrder
* InboundShipment
* InventoryLocation
* InventoryMovement
* InventoryBalance

⸻

Brand

A business vertical within SHÉ ESTATE.

Examples:

* SUMA
* TUFA
* GIDA
* SHÉ Rocks

Relationships:

* Brand ↔ Initiative
* Brand ↔ Item
* Brand ↔ Partner
* Brand ↔ SourcingTrip
* Brand ↔ Observation
* Brand ↔ Decision
* Brand ↔ PurchaseOrder
* Brand ↔ InboundShipment
* Brand ↔ InventoryLocation
* Brand ↔ InventoryMovement
* Brand ↔ InventoryBalance

Notes:

Brands are ecosystem hubs.

Most business activity ultimately belongs to one or more brands.

⸻

Initiative

A body of work.

Examples:

* YARD
* SUMA Packaging
* SGC Fundraiser

Relationships:

* Initiative ↔ Brand
* Initiative ↔ Item
* Initiative ↔ Partner
* Initiative ↔ SourcingTrip
* Initiative ↔ Observation
* Initiative ↔ Decision
* Initiative ↔ PurchaseOrder
* Initiative ↔ InboundShipment
* Initiative ↔ InventoryLocation
* Initiative ↔ InventoryMovement

Business Rule:

Inventory location participation is conditional.

Examples:

* SUMA Packaging may require warehousing.
* YARD may never require warehousing.
* SHÉ Rocks fundraising initiatives may never require warehousing.

⸻

Item

Represents materials, components, inventory, samples, products, packaging, and assets.

Examples:

* Human Hair Bundle
* Full Lace Cap
* Packaging Box
* Silk
* Lace
* Finished Wig
* Finished Garment
* Purse
* Home Goods

Relationships:

* Item ↔ Brand
* Item ↔ Initiative
* Item ↔ Partner
* Item ↔ SourcingTrip
* Item ↔ Observation
* Item ↔ Decision
* Item ↔ PurchaseOrder
* Item ↔ InboundShipment
* Item ↔ InventoryLocation
* Item ↔ InventoryMovement
* Item ↔ InventoryBalance

Notes:

Items are one of the primary entities within SHÉ OS.

Many observations, decisions, sourcing trips, purchase orders, inbound shipments, and inventory location interactions ultimately exist because of items.

An Item may connect to:

- an Inventory Balance
- an Inventory Movement
- an Inventory Location, when SHÉ tracks where that inventory is held

⸻

Partner

Represents external contributors.

Examples:

* Supplier
* Manufacturer
* Crafter
* Tailor
* Pattern Maker
* Technical Designer
* Logistics Provider

Relationships:

* Partner ↔ Brand
* Partner ↔ Initiative
* Partner ↔ Item
* Partner ↔ SourcingTrip
* Partner ↔ Observation
* Partner ↔ Decision
* Partner ↔ PurchaseOrder
* Partner ↔ InboundShipment
* Partner ↔ InventoryLocation
* Partner ↔ InventoryMovement
* Partner ↔ InventoryBalance

Business Rules:

One Partner → Many Purchase Orders

One Purchase Order → One Partner

A purchase order should have a single responsible partner.

Examples:

* One tailor
* One braider
* One beader
* One manufacturer

An inbound shipment may contain products from multiple partners.

Examples:

* Tailor
* Braider
* Beader
* Leather worker

Therefore:

One InboundShipment → Many Partners

One Partner → Many InboundShipments

⸻

SourcingTrip

Represents sourcing and research activity.

Examples:

* Vietnam 2026
* Morocco 2025
* China 2026
* Nigeria 2027

Relationships:

* SourcingTrip ↔ Brand
* SourcingTrip ↔ Initiative
* SourcingTrip ↔ Item
* SourcingTrip ↔ Partner
* SourcingTrip ↔ Observation
* SourcingTrip ↔ Decision
* SourcingTrip ↔ PurchaseOrder
* SourcingTrip ↔ InboundShipment

Business Rules:

Sourcing trips are expected to generate:

* Partners
* Observations
* Decisions
* Purchase Orders

Sourcing trips do not have a direct relationship to InventoryLocations.

Inventory location interactions occur through:

* Items
* Partners
* Purchase Orders
* Inbound Shipments
* Inventory Movements

not through the sourcing trip itself.

⸻

Observation

Represents learned knowledge.

Examples:

* Silk villages primarily produce raw silk.
* Bao Loc manufacturers are better suited for finished silk sourcing.
* Nigerian tailoring quality exceeded Vietnam for Collection 01.

Relationships:

* Observation ↔ Brand
* Observation ↔ Initiative
* Observation ↔ Item
* Observation ↔ Partner
* Observation ↔ SourcingTrip
* Observation ↔ Decision
* Observation ↔ PurchaseOrder
* Observation ↔ InboundShipment
* Observation ↔ InventoryLocation
* Observation ↔ InventoryMovement

Notes:

Observations provide context and evidence.

Observations should remain connected to the decisions and actions that result from them.

⸻

Decision

Represents intentional business choices.

Examples:

* Produce Collection 01 in Nigeria.
* Source silk from Bao Loc.
* Use drop shipping for SHÉ Rocks.

Relationships:

* Decision ↔ Brand
* Decision ↔ Initiative
* Decision ↔ Item
* Decision ↔ Partner
* Decision ↔ SourcingTrip
* Decision ↔ Observation
* Decision ↔ PurchaseOrder
* Decision ↔ InboundShipment
* Decision ↔ InventoryLocation
* Decision ↔ InventoryMovement

Notes:

Decisions should remain connected to the observations that informed them.

⸻

PurchaseOrder

Represents commitments to purchase goods or services.

Relationships:

* PurchaseOrder ↔ Brand
* PurchaseOrder ↔ Initiative
* PurchaseOrder ↔ Item
* PurchaseOrder ↔ Partner
* PurchaseOrder ↔ SourcingTrip
* PurchaseOrder ↔ Observation
* PurchaseOrder ↔ Decision
* PurchaseOrder ↔ InboundShipment
* PurchaseOrder ↔ InventoryLocation
* PurchaseOrder ↔ InventoryMovement

Business Rules:

One Purchase Order → One Partner

One Partner → Many Purchase Orders

A purchase order may or may not interact with an inventory location depending on the fulfillment model.

Examples:

SUMA

Purchase Order
→ Abuja warehouse
→ Customer

TUFA

Purchase Order
→ Crafter
→ Customer

SHÉ Rocks

Purchase Order
→ Vendor
→ Customer

Inventory location interaction is conditional.

A purchase order may be fulfilled across one or more inbound shipments.

⸻

InventoryLocation

Represents a physical or temporary place where SHÉ-owned inventory is tracked.

Examples:

* Abuja production location
* SHÉ Studio
* Abuja warehouse
* Africa Fashion Week DMV vendor location
* Temporary event storage

Relationships:

* InventoryLocation ↔ Brand
* InventoryLocation ↔ Initiative
* InventoryLocation ↔ Item
* InventoryLocation ↔ Partner
* InventoryLocation ↔ Observation
* InventoryLocation ↔ Decision
* InventoryLocation ↔ InventoryMovement
* InventoryLocation ↔ InventoryBalance

Business Rules:

Not every Item requires an InventoryLocation.

Made-to-order items may have no tracked inventory location before production.

Materials owned and stored by artisans are not SHÉ-controlled inventory unless SHÉ explicitly assumes ownership or requires tracking.

Inventory locations may be temporary.

An inventory location may remain in the historical record after it is no longer used.

Inventory location status may include:

* active
* inactive

Inactive locations remain connected to observations, decisions, inventory movements, and historical business activity.

Inventory location type may include:

* warehouse
* studio
* production_site
* event
* temporary_storage

⸻

InventoryMovement

Represents a recorded change to SHÉ-owned inventory.

Examples:

* Receiving finished wigs in Abuja
* Moving inventory to a SHÉ Studio
* Sending products to a vendor event
* Recording damaged inventory
* Recording lost inventory
* Consuming SHÉ-owned materials
* Correcting inventory after a physical count

Relationships:

* InventoryMovement ↔ Brand
* InventoryMovement ↔ Initiative
* InventoryMovement ↔ Item
* InventoryMovement ↔ Partner
* InventoryMovement ↔ PurchaseOrder
* InventoryMovement ↔ InventoryLocation
* InventoryMovement ↔ InboundShipment
* InventoryMovement ↔ Observation
* InventoryMovement ↔ Decision

Business Rules:

Every tracked inventory quantity change must be represented by an InventoryMovement.

Inventory movements preserve the historical reason inventory changed.

An inventory movement may increase, decrease, or transfer inventory.

A transfer between InventoryLocations must preserve both the source and destination and must record both the decrease at the source and the increase at the destination.

Inventory movements must not be deleted during normal application use.

⸻

InventoryBalance

Represents the current tracked quantity of an Item at an InventoryLocation.

Relationships:

* InventoryBalance ↔ Brand
* InventoryBalance ↔ Item
* InventoryBalance ↔ Partner
* InventoryBalance ↔ InventoryLocation

Business Rules:

An InventoryBalance is derived and maintained automatically from InventoryMovements.

An InventoryBalance must not be changed independently of an InventoryMovement.

Not every Item has an InventoryBalance.

Made-to-order items may have no balance until a physical item exists and SHÉ begins tracking it.

Items owned and stored by artisans are not included unless they are SHÉ-controlled inventory.

One Item may have balances at multiple InventoryLocations.

One InventoryLocation may contain balances for multiple Items.

⸻

Inbound Shipment

Represents movement of goods.

Relationships:

* InboundShipment ↔ Brand
* InboundShipment ↔ Initiative
* InboundShipment ↔ Item
* InboundShipment ↔ Partner
* InboundShipment ↔ SourcingTrip
* InboundShipment ↔ Observation
* InboundShipment ↔ Decision
* InboundShipment ↔ PurchaseOrder
* InboundShipment ↔ InventoryLocation
* InboundShipment ↔ InventoryMovement

Business Rules:

An inbound shipment may contain:

* Multiple purchase orders
* Multiple items
* Multiple partners
* Multiple brands

Examples:

One inbound shipment may contain:

* wigs from braiders
* garments from tailors
* bags from leather workers

Relationship:

One Inbound Shipment → One or  Many Purchase Orders

An inbound shipment may contain goods from one or more purchase orders.

Purchase order lines and inbound shipment lines must preserve which ordered quantities were shipped, received, accepted, damaged, or outstanding

Returns are not currently modeled.

Incorrect products are currently treated as:

* loss
* marketing inventory
* future rework inventory

Inventory location interaction is conditional.

⸻

## Future Domain Expansion

The following entities are expected to become part of SHÉ OS but are outside the scope of the current procurement and operations model:

COMMERCE - 
- Customer
- SalesOrder
- SalesOrderLine
- Payment
- Return