DOMAIN_MODEL.md

Core Objects

Brand

Represents a major business vertical.

Examples:

* SUMA
* TUFA
* GIDA
* SHÉ Rocks

⸻

Initiative

A project or body of work.

Examples:

* YARD
* SUMA Packaging
* SGC Fundraiser

⸻

Item

Any physical object.

Examples:

* Human Hair Bundle
* Butter Yellow Silk
* 13x6 Closure
* Finished Wig
* Packaging Box

⸻

Partner

Any external collaborator.

Types may include:

* Supplier
* Crafter
* Manufacturer
* Technical Designer
* Pattern Maker
* Logistics Partner

⸻

Sourcing Trip

Represents a research journey.

Examples:

* OrientalSpring'26: China, Vietnam, Macau, Korea
* 9jaNewYear'26: Nigeria
* AfroEuroSummer'25: France, Spain, Morocco, Portugal

⸻

Observation

A fact or lesson learned.

Example:
Silk villages primarily produce raw silk.

⸻

Decision

A business decision and the reasoning behind it.

Example:
Produce garments in Nigeria.

⸻

Inbound shipment

Movement of materials or products.

⸻

Purchase Order

Represents materials ordered from partners.

⸻

Inventory Movement

Represents a recorded change to SHÉ-owned inventory.

Examples:

* Receiving finished wigs from an inbound shipment
* Moving products from Abuja to a SHÉ Studio
* Sending products to a vendor event
* Recording damaged or lost inventory
* Consuming SHÉ-owned materials during production
* Correcting inventory after a physical count

⸻

Inventory Balance

Examples of items that may not have balances include:

* Made-to-order products that have not yet been produced
* Raw materials purchased and owned by an artisan
* Drop-shipped products that never enter SHÉ-controlled inventory

⸻

Inventory Location

Represents a place where SHÉ-owned inventory is intentionally
tracked.

Examples:

- Abuja production location
- SHÉ Studio
- Warehouse
- Temporary vendor-event location
- Temporary storage location

An Inventory Location may have a type such as:

- warehouse
- studio
- production_site
- event
- temporary_storage

⸻

Relationship Philosophy

Objects should not exist in isolation.

A single Item may connect to:

* a Brand
* an Initiative
* a Supplier
* a Sourcing Trip
* an Observation
* a Decision
* an Inbound shipment

The goal is to model relationships instead of isolated records.