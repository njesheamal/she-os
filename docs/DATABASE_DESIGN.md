# SHÉ OS Database Design

## Purpose

This document defines the relational database structure for the current SHÉ OS operational domain.

It translates the business concepts and relationship rules documented in:

- `DOMAIN_MODEL.md`
- `DOMAIN_RELATIONSHIPS.md`

into tables, keys, constraints, and association tables.

Customer-facing commerce concepts such as Customer, SalesOrder, Payment, and Return are outside the current implementation scope.

---

## Design Principles

- Use PostgreSQL as the primary database.
- Use UUID primary keys.
- Preserve relationships between operational and knowledge records.
- Avoid isolated records where meaningful business context exists.
- Use explicit association tables for meaningful many-to-many relationships.
- Support multiple SHÉ ESTATE brands and different fulfillment models.
- Do not assume every item passes through an inventory location.
- Keep customer commerce separate from internal procurement.
- Support partial and split fulfillment of purchase orders.
- Separate what was ordered from what was physically shipped and received.
- Distinguish ordered, shipped, received, and accepted quantities.
- Record every inventory change as an inventory movement.
- Maintain current inventory balances automatically from inventory movements.
- Do not allow inventory balances to be edited directly.

---

## Naming & Data Type Conventions

### Tables

Use lowercase plural snake_case names.

Examples:

- `brands`
- `purchase_orders`
- `sourcing_trips`

### Primary Keys

Use:

```
id
```

Each primary key will be a UUID.

### Foreign Keys

Use:

```
<singular_table_name>_id
```

Examples:

- `brand_id`
- `partner_id`
- `inventory_location_id`

### UUIDs

Primary keys and foreign keys use PostgreSQL UUID values.

UUIDs will be generated consistently using one approved strategy across all tables.

### Dates

Use `date` for values that do not require a time of day.

### Money

Monetary values use fixed-precision numeric fields.

Floating-point types must not be used for money.

Currency is stored separately using an ISO 4217 currency code.

### Quantities

Quantities use fixed-precision numeric fields so the system can support both whole and fractional amounts.

Examples include:

- individual products
- bundles
- yards
- meters
- kilograms
- liters

Quantities must not use floating-point types.

### Text

Use constrained string fields where maximum length has practical meaning.

Use text fields for unrestricted notes, descriptions, observations, and reasoning.

### Timestamps

Timestamps use timezone-aware PostgreSQL timestamp fields and are stored in UTC.

Standard timestamp fields:

- `created_at`
- `updated_at`

Additional timestamps should represent meaningful business events.

Examples:

- `ordered_at`
- `shipped_at`
- `delivered_at`
- `decided_at`

---

## Business Identifiers

UUID primary keys are internal database identifiers.

Records referenced by users should also have human-readable business identifiers where applicable.

Examples:

- purchase order number
- inbound shipment number
- item code or SKU
- initiative code

Business identifiers must have explicit uniqueness and mutability rules.

---

## Core Tables

### brands

### item_types

### items

### partner_types

### partners

### initiative_types

### initiatives

### sourcing_trips

### observations

### decisions

### units_of_measure

### purchase_orders

### purchase_order_lines

### inventory_location_types

### inventory_locations

### inbound_shipments

### inbound_shipment_lines

### inventory_movement_types

### inventory_movements

### inventory_balances

---

## Association Tables

Explicit association tables are used for approved many-to-many relationships that cannot be represented accurately through a single foreign key.

Association tables are not created for relationships that can be reliably derived through existing transactional records.

### Confirmed Association Tables

- `brand_initiatives`
- `brand_items`
- `brand_partners`
- `brand_sourcing_trips`
- `brand_observations`
- `brand_decisions`
- `brand_purchase_orders`
- `brand_inbound_shipments`
- `brand_inventory_locations`
- `initiative_items`
- `initiative_partners`
- `initiative_sourcing_trips`
- `initiative_observations`
- `initiative_decisions`
- `initiative_purchase_orders`
- `initiative_inbound_shipments`
- `initiative_inventory_locations`
- `sourcing_trip_items`
- `sourcing_trip_partners`
- `sourcing_trip_observations`
- `sourcing_trip_decisions`
- `sourcing_trip_purchase_orders`
- `sourcing_trip_inbound_shipments`
- `observation_decisions`
- `observation_items`
- `observation_partners`
- `observation_purchase_orders`
- `observation_inbound_shipments`
- `observation_inventory_locations`
- `observation_inventory_movements`
- `decision_items`
- `decision_partners`
- `decision_purchase_orders`
- `decision_inbound_shipments`
- `decision_inventory_locations`
- `decision_inventory_movements`
- `item_partners`

### Derived Relationships

The following relationships do not require separate association tables:

- Purchase Orders ↔ Inbound Shipments, derived through `purchase_order_lines` and `inbound_shipment_lines`
- Items ↔ Inbound Shipments, derived through `inbound_shipment_lines`
- Partners ↔ Inbound Shipments, derived through `purchase_orders`, `purchase_order_lines`, and `inbound_shipment_lines`
- Items ↔ Inventory Locations, derived through `inventory_balances` and `inventory_movements`
- Inventory Balances ↔ Inventory Movements, because balances are maintained from movements

### Association Table Structure

Unless an association has its own business attributes, confirmed association tables use the following shared structure:

- Two UUID foreign-key columns referencing the associated tables
- A composite primary key containing both foreign keys
- No separate `id` column
- An additional index on the second foreign-key column
- No duplicate relationship rows
- No independent status or deletion lifecycle

Example:
initiative_items
initiative_id UUID
item_id UUID

PRIMARY KEY (initiative_id, item_id)
FOREIGN KEY (initiative_id) REFERENCES initiatives(id)
FOREIGN KEY (item_id) REFERENCES items(id)
INDEX (item_id)


### Association Table Keys

- `brand_initiatives`: `brand_id`, `initiative_id`
- `brand_items`: `brand_id`, `item_id`
- `brand_partners`: `brand_id`, `partner_id`
- `brand_sourcing_trips`: `brand_id`, `sourcing_trip_id`
- `brand_observations`: `brand_id`, `observation_id`
- `brand_decisions`: `brand_id`, `decision_id`
- `brand_purchase_orders`: `brand_id`, `purchase_order_id`
- `brand_inbound_shipments`: `brand_id`, `inbound_shipment_id`
- `brand_inventory_locations`: `brand_id`, `inventory_location_id`

- `initiative_items`: `initiative_id`, `item_id`
- `initiative_partners`: `initiative_id`, `partner_id`
- `initiative_sourcing_trips`: `initiative_id`, `sourcing_trip_id`
- `initiative_observations`: `initiative_id`, `observation_id`
- `initiative_decisions`: `initiative_id`, `decision_id`
- `initiative_purchase_orders`: `initiative_id`, `purchase_order_id`
- `initiative_inbound_shipments`: `initiative_id`, `inbound_shipment_id`
- `initiative_inventory_locations`: `initiative_id`, `inventory_location_id`

- `sourcing_trip_items`: `sourcing_trip_id`, `item_id`
- `sourcing_trip_partners`: `sourcing_trip_id`, `partner_id`
- `sourcing_trip_observations`: `sourcing_trip_id`, `observation_id`
- `sourcing_trip_decisions`: `sourcing_trip_id`, `decision_id`
- `sourcing_trip_purchase_orders`: `sourcing_trip_id`, `purchase_order_id`
- `sourcing_trip_inbound_shipments`: `sourcing_trip_id`, `inbound_shipment_id`

- `observation_decisions`: `observation_id`, `decision_id`
- `observation_items`: `observation_id`, `item_id`
- `observation_partners`: `observation_id`, `partner_id`
- `observation_purchase_orders`: `observation_id`, `purchase_order_id`
- `observation_inbound_shipments`: `observation_id`, `inbound_shipment_id`
- `observation_inventory_locations`: `observation_id`, `inventory_location_id`
- `observation_inventory_movements`: `observation_id`, `inventory_movement_id`

- `decision_items`: `decision_id`, `item_id`
- `decision_partners`: `decision_id`, `partner_id`
- `decision_purchase_orders`: `decision_id`, `purchase_order_id`
- `decision_inbound_shipments`: `decision_id`, `inbound_shipment_id`
- `decision_inventory_locations`: `decision_id`, `inventory_location_id`
- `decision_inventory_movements`: `decision_id`, `inventory_movement_id`

- `item_partners`: `item_id`, `partner_id`

---

## Status Values

Where possible, SHÉ OS uses a consistent status vocabulary across domains.

### Brand Status

- active
- inactive

---

### Item Status

- active
- inactive
- discontinued

---

### Partner Status

- active
- inactive

---

### Initiative Status

- planned
- active
- on_hold
- completed
- cancelled

---

### Sourcing Trip Status

- planned
- in_progress
- completed
- cancelled

---

### Decision Status

- proposed
- approved
- in_effect
- superseded
- archived

---

### Purchase Order Status

- draft
- submitted
- accepted
- in_production
- partially_fulfilled
- fulfilled
- cancelled

---

### Inbound Shipment Status

- preparing
- in_transit
- partially_received
- received
- closed

---

### Inventory Location Status

- active
- inactive

---

## Type Values

The following lookup tables define classifications used throughout SHÉ OS.

### Item Types

- material
- component
- sample
- finished_product
- packaging
- asset

### Partner Types

- supplier
- manufacturer
- crafter
- tailor
- pattern_maker
- technical_designer
- logistics_provider

### Initiative Types

- collection
- research
- social_impact_program

### Inventory Location Types

- warehouse
- studio
- production_site
- event
- temporary_storage

### Inventory Movement Types

- receipt
- transfer_in
- transfer_out
- adjustment_in
- adjustment_out
- damage
- loss
- consumption
- sample
- return_to_stock

### Units of Measure

- piece
- bundle
- set
- pair
- yard
- meter
- centimeter
- kilogram
- gram
- liter
- milliliter
- roll
- spool
- box
- carton

---

## Deletion Strategy

Determine which records may be:

- hard deleted
- archived
- deactivated
- preserved permanently for historical integrity

Operational records such as purchase orders, inbound shipments, inventory_movements, observations, and decisions should generally remain part of the historical record.

---

## Lookup Table Management

Lookup table records should follow these guidelines:

- Add → insert a row
- Rename → update the name or description while preserving the slug where practical
- Retire → set `is_active = false`
- Delete → only when the record has never been referenced

---

## Table Definitions

Each table definition should include:

- Purpose
- Columns
- Primary key
- Foreign keys
- Unique constraints
- Nullability rules
- Check constraints
- Indexes
- Relationships
- Deletion behavior

### brands

#### Purpose

Stores the major business verticals within SHÉ ESTATE.

Examples:

- SUMA
- TUFA
- GIDA
- SHÉ Rocks

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the brand |
| `slug` | VARCHAR | No | Stable machine-readable brand identifier |
| `description` | TEXT | Yes | Description of the brand |
| `status` | VARCHAR | No | Current brand status |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `status` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.
- `status` must contain an approved brand status value.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `status` if brand filtering requires it

#### Relationships

A Brand may relate to:

- Initiatives
- Items
- Partners
- Sourcing Trips
- Observations
- Decisions
- Purchase Orders
- Inbound Shipments
- Inventory Locations
- Inventory Movements
- Inventory Balances

The specific foreign keys or association tables will be defined under the relevant related tables.

#### Deletion Behavior

Brands referenced by operational or historical records must not be hard deleted.

A brand that is no longer operating should be deactivated through its status while preserving its relationships and historical records.

---

### item_types

#### Purpose

Stores the classifications used to organize Items.

Examples may include:

- material
- component
- sample
- finished product
- packaging
- asset

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the item type |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the item type |
| `is_active` | BOOLEAN | No | Whether the item type is available for current use |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `is_active` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `is_active` if frequently used for filtering

#### Relationships

- One ItemType may classify many Items.

- Each Item must belong to one ItemType.

#### Deletion Behavior

An ItemType referenced by an Item must not be hard deleted.

Item types that are no longer used should be made inactive.

---

### items

#### Purpose

Stores physical objects tracked within SHÉ OS.

Items may represent:

- materials
- components
- inventory
- samples
- finished products
- packaging
- assets

Examples include Human Hair Bundles, Full Lace Caps, Silk, Finished Wigs, Finished Garments, and Packaging Boxes.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the item |
| `slug` | VARCHAR | No | Stable machine-readable item identifier |
| `sku` | VARCHAR | Yes | Human-readable stock or catalog identifier |
| `item_type_id` | UUID | No | Item classification |
| `description` | TEXT | Yes | Item description |
| `status` | VARCHAR | No | Current item status |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `item_type_id` references `item_types.id`

Item relationships that are many-to-many will be implemented through association tables.

#### Unique Constraints

- `slug`
- `sku`, when present

`name` should not be globally unique because different brands or item categories may use the same display name.

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `item_type_id` is required.
- `status` is required.
- `sku` is optional.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.
- `sku` must not be empty when provided.
- `status` must contain an approved item status value.

#### Indexes

- Unique index on `slug`
- Unique partial index on `sku` where `sku` is not null
- Index on `item_type_id`
- Index on `status`

#### Relationships

An Item may relate to:

- Brands
- Initiatives
- Partners
- Sourcing Trips
- Observations
- Decisions
- Purchase Orders through Purchase Order Lines
- Inbound Shipments through Inbound Shipment Lines
- Inventory Locations
- Inventory Movements
- Inventory Balances
- Each Item belongs to one ItemType.
- One ItemType may classify many Items.

Not every Item requires inventory tracking or an Inventory Location.

Made-to-order products may have no inventory balance before production. Materials owned and stored by artisans are not treated as SHÉ-controlled inventory unless SHÉ explicitly assumes ownership or requires tracking.

#### Deletion Behavior

Items referenced by operational, inventory, or historical records must not be hard deleted.

Items that are no longer used should be archived or deactivated through their status while preserving existing relationships and history.

---

### partner_types

#### Purpose

Stores the classifications used to organize Partners.

Examples may include:

- supplier
- manufacturer
- crafter
- tailor
- pattern maker
- technical designer
- logistics provider

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the partner type |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the partner type |
| `is_active` | BOOLEAN | No | Whether the partner type is available for current use |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `is_active` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `is_active` if frequently used for filtering

#### Relationships

- One PartnerType may classify many Partners.

- Each Partner must belong to one PartnerType.

#### Deletion Behavior

Partner types referenced by Partners must not be hard deleted.

Partner types that are no longer used should be made inactive.

---

### partners

#### Purpose

Stores external individuals and organizations that collaborate with SHÉ ESTATE.

Partners may represent:

- suppliers
- manufacturers
- crafters
- tailors
- pattern makers
- technical designers
- logistics providers

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the partner |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `partner_type_id` | UUID | No | Classification of the partner |
| `description` | TEXT | Yes | Description or notes |
| `status` | VARCHAR | No | Current partner status |
| `website` | VARCHAR | Yes | Website URL |
| `email` | VARCHAR | Yes | Primary contact email |
| `phone` | VARCHAR | Yes | Primary contact phone number |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `partner_type_id` references `partner_types.id`

#### Unique Constraints

- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `partner_type_id` is required.
- `status` is required.
- `description` is optional.
- `website` is optional.
- `email` is optional.
- `phone` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.
- `status` must contain an approved partner status value.

#### Indexes

- Unique index on `slug`
- Index on `partner_type_id`
- Index on `status`

#### Relationships

A Partner may relate to:

- Brands
- Initiatives
- Items
- Sourcing Trips
- Observations
- Decisions
- Purchase Orders
- Inbound Shipments

A Partner may have many Purchase Orders.

Each Purchase Order belongs to exactly one Partner.

#### Deletion Behavior

Follow the global Deletion Strategy.

---

### initiative_types

#### Purpose

Stores the classifications used to organize Initiatives.

Examples may include:

- collection
- research
- social_impact_program

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the initiative type |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the initiative type |
| `is_active` | BOOLEAN | No | Whether the initiative type is available for current use |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `is_active` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `is_active` if frequently used for filtering

#### Relationships

- One InitiativeType may classify many Initiatives.

- Each Initiative must belong to one InitiativeType.

#### Deletion Behavior

Initiative types referenced by Initiatives must not be hard deleted.

Initiative types that are no longer used should be made inactive.

---

### initiatives

#### Purpose

Stores projects, programs, and bodies of work within SHÉ ESTATE.

Examples include:

- YARD
- SUMA Packaging
- SGC Fundraiser

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `initiative_type_id` | UUID | No | Classification of the initiative |
| `name` | VARCHAR | No | Display name of the initiative |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the initiative |
| `status` | VARCHAR | No | Current initiative status |
| `start_date` | DATE | Yes | Planned or actual start date |
| `end_date` | DATE | Yes | Planned or actual completion date |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `initiative_type_id` references `initiative_types.id`

#### Unique Constraints

- `slug`

#### Nullability Rules

- `id` is required.
- `initiative_type_id` is required.
- `name` is required.
- `slug` is required.
- `status` is required.
- `description` is optional.
- `start_date` is optional.
- `end_date` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.
- `status` must contain an approved initiative status value.
- `end_date`, when present, must not occur before `start_date`.

#### Indexes

- Unique index on `slug`
- Index on `initiative_type_id`
- Index on `status`
- Index on `start_date`

#### Relationships

An Initiative may relate to:

- Brands
- Items
- Partners
- Sourcing Trips
- Observations
- Decisions
- Purchase Orders
- Inbound Shipments
- Inventory Locations
- Inventory Movements
- Each Initiative belongs to one InitiativeType.
- One InitiativeType may classify many Initiatives.

Warehouse participation is conditional and is represented through Inventory Locations when inventory tracking is required.

#### Deletion Behavior

Follow the global Deletion Strategy.

---

### sourcing_trips

#### Purpose

Stores planned and completed sourcing trips that connect SHÉ ESTATE with suppliers, makers, and partner locations.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the sourcing trip |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the trip |
| `status` | VARCHAR | No | Current sourcing trip status |
| `start_date` | DATE | Yes | Date the trip began or is expected to begin |
| `end_date` | DATE | Yes | Date the trip ended or is expected to end |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `status` is required.
- `description` is optional.
- `start_date` is optional.
- `end_date` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.
- `status` must contain an approved sourcing trip status value.
- `end_date`, when present, must not occur before `start_date`.

#### Indexes

- Unique index on `slug`
- Index on `status`
- Index on `start_date`

#### Relationships

A Sourcing Trip may relate to:

- Initiatives
- Brands
- Items
- Partners
- Observations
- Decisions
- Purchase Orders
- Inbound Shipments

The specific foreign keys or association tables will be defined under the relevant related tables.

#### Deletion Behavior

Sourcing trips referenced by operational or historical records must not be hard deleted.

A sourcing trip that is no longer active should be deactivated through its status while preserving its history.

---

### observations

#### Purpose

Stores recorded facts, lessons, and insights captured during sourcing, production, and operational work.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `title` | VARCHAR | No | Short title identifying the observation |
| `details` | TEXT | No | The fact, lesson, or insight recorded |
| `observed_at` | TIMESTAMPTZ | Yes | When the observation was made |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- None

#### Nullability Rules

- `id` is required.
- `title` is required.
- `details` is required.
- `observed_at` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `title` must not be empty.
- `details` must not be empty.

#### Indexes

- Index on `observed_at`

#### Relationships

An Observation may relate to:

- Initiatives
- Brands
- Items
- Partners
- Sourcing Trips
- Decisions
- Purchase Orders

The specific foreign keys or association tables will be defined under the relevant related tables.

#### Deletion Behavior

Observations should be preserved as historical records and not hard deleted when they are referenced by other business entities.

---

### decisions

#### Purpose

Stores business choices, governance outcomes, and the reasoning behind them.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `title` | VARCHAR | No | Short title identifying the decision |
| `decision_summary` | TEXT | No | The business choice that was made |
| `reasoning` | TEXT | Yes | Reasoning supporting the decision |
| `status` | VARCHAR | No | Current decision status |
| `decided_at` | TIMESTAMPTZ | Yes | When the decision was made |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- None

#### Nullability Rules

- `id` is required.
- `title` is required.
- `decision_summary` is required.
- `status` is required.
- `reasoning` is optional.
- `decided_at` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `title` must not be empty.
- `decision_summary` must not be empty.
- `status` must contain an approved decision status value.

#### Indexes

- Index on `status`
- Index on `decided_at`

#### Relationships

A Decision may relate to:

- Initiatives
- Brands
- Items
- Partners
- Sourcing Trips
- Observations
- Purchase Orders

The specific foreign keys or association tables will be defined under the relevant related tables.

#### Deletion Behavior

Decisions should remain part of the historical record and must not be hard deleted when referenced by business records.

---

### purchase_orders

#### Purpose

Stores purchase orders issued to partners, capturing the business transaction and partner relationship that drives procurement.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `purchase_order_number` | VARCHAR | No | Human-readable purchase order identifier |
| `partner_id` | UUID | No | Partner responsible for fulfilling the purchase order |
| `status` | VARCHAR | No | Current purchase order status |
| `order_date` | DATE | Yes | Date the purchase order was created |
| `expected_date` | DATE | Yes | Expected delivery or fulfillment date |
| `currency_code` | CHAR(3) | Yes | ISO 4217 currency code for the order |
| `notes` | TEXT | Yes | Additional purchase order notes |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `partner_id` references `partners.id`

#### Unique Constraints

- `purchase_order_number`

#### Nullability Rules

- `id` is required.
- `purchase_order_number` is required.
- `partner_id` is required.
- `status` is required.
- `order_date` is required.
- `expected_date` is optional.
- `currency_code` is optional.
- `notes` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `purchase_order_number` must not be empty.
- `status` must contain an approved purchase order status value.
- `currency_code`, when present, must be a valid ISO 4217 code.
- `expected_date`, when present, must not occur before `order_date`.

#### Indexes

- Unique index on `purchase_order_number`
- Index on `partner_id`
- Index on `status`
- Index on `order_date`

#### Relationships

A Purchase Order belongs to one Partner.

A Purchase Order may relate to:

- Brands
- Initiatives
- Sourcing Trips
- Observations
- Decisions
- Inbound Shipments

#### Deletion Behavior

Purchase Orders referenced by lines, shipments, or inventory records must not be hard deleted.

An archived purchase order should preserve its line items for audit.

---

### units_of_measure

#### Purpose

Stores standard units of measure used throughout procurement and inventory tracking.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the unit of measure |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the unit |
| `is_active` | BOOLEAN | No | Whether the unit is available for current use |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `is_active` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `is_active`

#### Relationships

Units of measure may be referenced by Purchase Order Lines, Inbound Shipment Lines, Inventory Movements, and Inventory Balances.

#### Deletion Behavior

Units of measure referenced by transactional or inventory records must not be hard deleted.

Inactive units should remain available for historical reference.

---

### purchase_order_lines

#### Purpose

Stores individual line items within a purchase order, capturing the ordered quantity, unit pricing, and transaction-specific details.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `purchase_order_id` | UUID | No | Purchase order containing the line |
| `item_id` | UUID | No | Item being ordered |
| `line_number` | INTEGER | No | Position of the line within the purchase order |
| `description` | TEXT | Yes | Transaction-specific item description |
| `quantity_ordered` | NUMERIC | No | Quantity ordered |
| `unit_of_measure_id` | UUID | No | Unit of measure for the ordered quantity |
| `unit_price` | NUMERIC | Yes | Price per unit at the time of ordering |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `purchase_order_id` references `purchase_orders.id`
- `item_id` references `items.id`
- `unit_of_measure_id` references `units_of_measure.id`

#### Unique Constraints

- `purchase_order_id`, `line_number`

#### Nullability Rules

- `id` is required.
- `purchase_order_id` is required.
- `item_id` is required.
- `line_number` is required.
- `quantity_ordered` is required.
- `unit_of_measure_id` is required.
- `description` is optional.
- `unit_price` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `line_number` must be greater than zero.
- `quantity_ordered` must be greater than or equal to zero. 
- `unit_price`, when present, must be greater than or equal to zero.

#### Indexes

- Unique index on (`purchase_order_id`, `line_number`)
- Index on `purchase_order_id`
- Index on `item_id`

#### Relationships

A Purchase Order Line belongs to one Purchase Order and one Item.

A Purchase Order Line may be referenced by one or more Inbound Shipment Lines.

#### Deletion Behavior

Purchase Order Lines referenced by shipment or receipt records must not be hard deleted.

When a Purchase Order is archived, its lines should remain available for historical audit.

---

### inbound_shipments

#### Purpose

Stores inbound shipment records for goods that are dispatched by partners and received into SHÉ OS inventory.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `inbound_shipment_number` | VARCHAR | No | Human-readable inbound shipment identifier |
| `status` | VARCHAR | No | Current inbound shipment status |
| `tracking_number` | VARCHAR | Yes | Carrier tracking number |
| `carrier_name` | VARCHAR | Yes | Carrier used for the shipment |
| `destination_inventory_location_id` | UUID | Yes | Tracked destination receiving the shipment |
| `shipped_at` | TIMESTAMPTZ | Yes | When the shipment was dispatched |
| `received_at` | TIMESTAMPTZ | Yes | When the shipment was physically received |
| `notes` | TEXT | Yes | Additional shipment notes |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `destination_inventory_location_id` references `inventory_locations.id`

#### Unique Constraints

- `inbound_shipment_number`

#### Nullability Rules

- `id` is required.
- `inbound_shipment_number` is required.
- `status` is required.
- `tracking_number` is optional.
- `carrier_name` is optional.
- `destination_inventory_location_id` is optional.
- `shipped_at` is optional.
- `received_at` is optional.
- `notes` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `inbound_shipment_number` must not be empty.
- `status` must contain an approved inbound shipment status value.
- `received_at`, when present, must not occur before `shipped_at`.

#### Indexes

- Unique index on `inbound_shipment_number`
- Index on `status`
- Index on `destination_inventory_location_id`
- Index on `shipped_at`
- Index on `received_at`

#### Relationships

An Inbound Shipment may relate to:

- Partners
- Purchase Orders
- Inbound Shipment Lines
- Inventory Locations

The specific foreign keys or association tables will be defined under the relevant related tables.

#### Deletion Behavior

Inbound Shipments referenced by receiving and inventory records must not be hard deleted.

Shipment history should be preserved for audit and reconciliation.

---

### inbound_shipment_lines

#### Purpose

Stores each line included in an inbound shipment and the quantities received, accepted, and damaged.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `inbound_shipment_id` | UUID | No | Inbound shipment containing the line |
| `purchase_order_line_id` | UUID | No | Purchase order line being fulfilled |
| `quantity_shipped` | NUMERIC | No | Quantity dispatched by the partner |
| `quantity_received` | NUMERIC | Yes | Quantity physically received |
| `quantity_accepted` | NUMERIC | Yes | Quantity accepted after receipt |
| `quantity_damaged` | NUMERIC | Yes | Quantity received in damaged condition |
| `unit_of_measure_id` | UUID | No | Unit of measure for shipment quantities |
| `notes` | TEXT | Yes | Receiving or condition notes |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `inbound_shipment_id` references `inbound_shipments.id`
- `purchase_order_line_id` references `purchase_order_lines.id`
- `unit_of_measure_id` references `units_of_measure.id`

#### Unique Constraints

- `inbound_shipment_id`, `purchase_order_line_id`

#### Nullability Rules

- `id` is required.
- `inbound_shipment_id` is required.
- `purchase_order_line_id` is required.
- `quantity_shipped` is required.
- `unit_of_measure_id` is required.
- `quantity_received` is optional.
- `quantity_accepted` is optional.
- `quantity_damaged` is optional.
- `notes` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `quantity_shipped` must be greater than or equal to zero.
- `quantity_received`, when present, must be greater than or equal to zero.
- `quantity_accepted`, when present, must be greater than or equal to zero.
- `quantity_damaged`, when present, must be greater than or equal to zero.

#### Indexes

- Unique index on (`inbound_shipment_id`, `purchase_order_line_id`)
- Index on `inbound_shipment_id`
- Index on `purchase_order_line_id`

#### Relationships

An Inbound Shipment Line belongs to one Inbound Shipment and one Purchase Order Line.

It may be used to drive inventory receipts and movement records.

#### Deletion Behavior

Inbound Shipment Lines should remain available for audit and must not be hard deleted when referenced by inventory or receipt records.

---

### inventory_location_types

#### Purpose

Stores classifications for inventory locations used across SHÉ OS.

Examples include:

- warehouse
- studio
- production_site
- event
- temporary_storage

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the inventory location type |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the location type |
| `is_active` | BOOLEAN | No | Whether the type is available for current use |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `is_active` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `is_active`

#### Relationships

- One InventoryLocationType may classify many InventoryLocations.

- Each InventoryLocation must belong to one InventoryLocationType.

#### Deletion Behavior

Inventory location types referenced by inventory locations must not be hard deleted.

Inactive types should remain available for historical reference.

---

### inventory_locations

#### Purpose

Stores physical and virtual locations where inventory is received, held, or moved.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `inventory_location_type_id` | UUID | No | Classification of the inventory location |
| `name` | VARCHAR | No | Display name of the location |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description or purpose of the location |
| `status` | VARCHAR | No | Current inventory location status |
| `address_line_1` | VARCHAR | Yes | Primary street address |
| `address_line_2` | VARCHAR | Yes | Additional address information |
| `city` | VARCHAR | Yes | City |
| `region` | VARCHAR | Yes | State, province, or region |
| `postal_code` | VARCHAR | Yes | Postal code |
| `country_code` | CHAR(2) | Yes | ISO 3166-1 alpha-2 country code |
| `active_from` | TIMESTAMPTZ | Yes | When the location became operational |
| `active_until` | TIMESTAMPTZ | Yes | When a temporary or inactive location stopped operating |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `inventory_location_type_id` references `inventory_location_types.id`

#### Unique Constraints

- `slug`

#### Nullability Rules

- `id` is required.
- `inventory_location_type_id` is required.
- `name` is required.
- `slug` is required.
- `status` is required.
- `description` is optional.
- `address_line_1` is optional.
- `address_line_2` is optional.
- `city` is optional.
- `region` is optional.
- `postal_code` is optional.
- `country_code` is optional.
- `active_from` is optional.
- `active_until` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.
- `status` must contain an approved inventory location status value.
- `country_code`, when present, must be a valid two-character ISO 3166-1 alpha-2 code.
- `active_until`, when present, must not occur before `active_from`.

#### Indexes

- Unique index on `slug`
- Index on `inventory_location_type_id`
- Index on `status`
- Index on `city`
- Index on `country_code`

#### Relationships

An Inventory Location belongs to one Inventory Location Type.

An Inventory Location may relate to:

- Inbound Shipments
- Inventory Movements
- Inventory Balances

#### Deletion Behavior

Inventory Locations referenced by inventory or shipment records must not be hard deleted.

Locations that are no longer used should be deactivated through status while preserving inventory history.

---

### inventory_movement_types

#### Purpose

Stores classifications for the types of inventory movements tracked by SHÉ OS.

Examples may include:

- receipt
- transfer_in
- transfer_out
- adjustment_in
- adjustment_out
- damage
- loss
- consumption
- sample
- return_to_stock

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `name` | VARCHAR | No | Display name of the inventory movement type |
| `slug` | VARCHAR | No | Stable machine-readable identifier |
| `description` | TEXT | Yes | Description of the movement type |
| `is_active` | BOOLEAN | No | Whether the type is available for current use |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- None

#### Unique Constraints

- `name`
- `slug`

#### Nullability Rules

- `id` is required.
- `name` is required.
- `slug` is required.
- `is_active` is required.
- `description` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `name` must not be empty.
- `slug` must not be empty.

#### Indexes

- Unique index on `name`
- Unique index on `slug`
- Index on `is_active`

#### Relationships

- One InventoryMovementType may classify many InventoryMovements.

- Each InventoryMovement must belong to one InventoryMovementType.

#### Deletion Behavior

Inventory movement types referenced by inventory movements must not be hard deleted.

Inactive movement types should remain available for historical reference.

---

### inventory_movements

#### Purpose

Stores every tracked change to inventory quantities across locations.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `item_id` | UUID | No | Item whose inventory changed |
| `inventory_location_id` | UUID | No | Location where the quantity changed |
| `inventory_movement_type_id` | UUID | No | Classification of the movement |
| `inbound_shipment_line_id` | UUID | Yes | Shipment line responsible for a receipt movement |
| `related_movement_id` | UUID | Yes | Related movement, such as the other side of a transfer |
| `quantity_delta` | NUMERIC | No | Signed quantity added to or removed from inventory |
| `unit_of_measure_id` | UUID | No | Unit of measure for the movement quantity |
| `occurred_at` | TIMESTAMPTZ | No | When the inventory change occurred |
| `notes` | TEXT | Yes | Explanation or supporting details |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent update timestamp |

#### Primary Key

- `id`

#### Foreign Keys

- `item_id` references `items.id`
- `inventory_location_id` references `inventory_locations.id`
- `inventory_movement_type_id` references `inventory_movement_types.id`
- `inbound_shipment_line_id` references `inbound_shipment_lines.id`
- `related_movement_id` references `inventory_movements.id`
- `unit_of_measure_id` references `units_of_measure.id`

#### Unique Constraints

- None

#### Nullability Rules

- `id` is required.
- `item_id` is required.
- `inventory_location_id` is required.
- `inventory_movement_type_id` is required.
- `quantity_delta` is required.
- `unit_of_measure_id` is required.
- `occurred_at` is required.
- `inbound_shipment_line_id` is optional.
- `related_movement_id` is optional.
- `notes` is optional.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `quantity_delta` must not equal zero.

#### Indexes

- Index on `item_id`
- Index on `inventory_location_id`
- Index on `inventory_movement_type_id`
- Index on `occurred_at`

#### Relationships

An Inventory Movement belongs to one Item, one Inventory Location, and one Inventory Movement Type.

It may optionally reference an Inbound Shipment Line or a related movement record.

#### Deletion Behavior

Inventory Movements are historical audit records and must not be hard deleted when referenced by balances or reports.

---

### inventory_balances

#### Purpose

Stores the current tracked balance for each item at each inventory location.

#### Columns

| Column | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID | No | Primary key |
| `item_id` | UUID | No | Item whose current quantity is stored |
| `inventory_location_id` | UUID | No | Location where the item is held |
| `quantity_on_hand` | NUMERIC | No | Current tracked quantity |
| `unit_of_measure_id` | UUID | No | Canonical unit of measure for this item/location balance |
| `created_at` | TIMESTAMPTZ | No | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | No | Most recent automatic balance update |

#### Primary Key

- `id`

#### Foreign Keys

- `item_id` references `items.id`
- `inventory_location_id` references `inventory_locations.id`
- `unit_of_measure_id` references `units_of_measure.id`

#### Unique Constraints

- `item_id`, `inventory_location_id`

This assumes each item-location pair is tracked in a single canonical unit of measure.

#### Nullability Rules

- `id` is required.
- `item_id` is required.
- `inventory_location_id` is required.
- `quantity_on_hand` is required.
- `unit_of_measure_id` is required.
- `created_at` is required.
- `updated_at` is required.

#### Check Constraints

- `quantity_on_hand` must be greater than or equal to zero.

#### Indexes

- Unique index on (`item_id`, `inventory_location_id`)
- Index on `item_id`
- Index on `inventory_location_id`

#### Relationships

An Inventory Balance belongs to one Item and one Inventory Location.

Inventory Balances are derived from Inventory Movements and should not be edited directly.

#### Deletion Behavior

Inventory Balances represent current derived state rather than a historical record.

Depending on the chosen policy, a balance row may be removed when an item-location quantity reaches zero and no longer requires an active row.

Inventory Movements preserve the history of how balances changed.

---

## Future Expansion

The current database models internal operations only.

The schema is intentionally designed to support future customer commerce without restructuring existing procurement or inventory tables.

Future domains include:

- Customer
- SalesOrder
- SalesOrderLine
- Payment
- CustomerShipment
- CustomerShipmentLine
- Return
- Refund