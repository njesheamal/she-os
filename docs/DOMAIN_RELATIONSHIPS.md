Here’s the version I would actually commit based on the matrix and the corrections we’ve made.

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
* Shipment
* Warehouse

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
* Brand ↔ Shipment
* Brand ↔ Warehouse

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
* Initiative ↔ Shipment
* Initiative ↔ Warehouse

Business Rule:

Warehouse participation is conditional.

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
* Item ↔ Shipment
* Item ↔ Warehouse

Notes:

Items are one of the primary entities within SHÉ OS.

Many observations, decisions, sourcing trips, purchase orders, shipments, and warehouse interactions ultimately exist because of items.

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
* Partner ↔ Shipment
* Partner ↔ Warehouse

Business Rules:

One Partner → Many Purchase Orders

One Purchase Order → One Partner

A purchase order should have a single responsible partner.

Examples:

* One tailor
* One braider
* One beader
* One manufacturer

A shipment may contain products from multiple partners.

Examples:

* Tailor
* Braider
* Beader
* Leather worker

Therefore:

One Shipment → Many Partners

One Partner → Many Shipments

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
* SourcingTrip ↔ Shipment

Business Rules:

Sourcing trips are expected to generate:

* Partners
* Observations
* Decisions
* Purchase Orders

Sourcing trips do not have a direct relationship to warehouses.

Warehouse interactions occur through:

* Items
* Partners
* Purchase Orders
* Shipments

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
* Observation ↔ Shipment
* Observation ↔ Warehouse

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
* Decision ↔ Shipment
* Decision ↔ Warehouse

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
* PurchaseOrder ↔ Shipment
* PurchaseOrder ↔ Warehouse

Business Rules:

One Purchase Order → One Partner

One Partner → Many Purchase Orders

A purchase order may or may not interact with a warehouse depending on the fulfillment model.

Examples:

SUMA

Purchase Order
→ Warehouse
→ Customer

TUFA

Purchase Order
→ Crafter
→ Customer

SHÉ Rocks

Purchase Order
→ Vendor
→ Customer

Warehouse interaction is conditional.

A purchase order can only be shipped once.

⸻

Shipment

Represents movement of goods.

Relationships:

* Shipment ↔ Brand
* Shipment ↔ Initiative
* Shipment ↔ Item
* Shipment ↔ Partner
* Shipment ↔ SourcingTrip
* Shipment ↔ Observation
* Shipment ↔ Decision
* Shipment ↔ PurchaseOrder
* Shipment ↔ Warehouse

Business Rules:

A shipment may contain:

* Multiple purchase orders
* Multiple items
* Multiple partners
* Multiple brands

Examples:

One shipment may contain:

* wigs from braiders
* garments from tailors
* bags from leather workers

Relationship:

One Shipment → Many Purchase Orders

One Purchase Order → One Shipment

Purchase orders cannot be split across multiple shipments.

Returns are not currently modeled.

Incorrect products are currently treated as:

* loss
* marketing inventory
* future rework inventory

Warehouse interaction is conditional.

⸻

Warehouse

Represents storage and fulfillment locations.

Relationships:

* Warehouse ↔ Brand
* Warehouse ↔ Initiative
* Warehouse ↔ Item
* Warehouse ↔ Partner
* Warehouse ↔ Observation
* Warehouse ↔ Decision
* Warehouse ↔ PurchaseOrder
* Warehouse ↔ Shipment

Business Rules:

Warehouse participation depends on business model.

Examples:

SUMA
Warehouse likely.

TUFA
Warehouse may or may not be involved.

GIDA
Warehouse may or may not be involved depending on product type.

SHÉ Rocks
Typically no SHÉ-controlled inventory.

Warehouse relationships should be evaluated through operational workflows rather than assumed universally.

1. **SourcingTrip has no direct Warehouse relationship.**
2. **PurchaseOrder belongs to exactly one Partner.**
3. **Warehouse participation is conditional for both Initiatives and PurchaseOrders.**



## Future Domain Expansion

The following entities are expected to become part of SHÉ OS but are outside the scope of the current procurement and operations model:

COMMERCE - 
- Customer
- SalesOrder
- SalesOrderLine
- Payment
- Return