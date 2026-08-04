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

## Naming Conventions

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

### Timestamps

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

## Core Tables

### brands

### items

### partners

### sourcing_trips

### observations

### decisions

### initiatives

### purchase_orders

### purchase_order_lines

### inbound_shipments

### inbound_shipment_lines

### inventory_movements

### inventory_balances

### inventory_locations

---

## Association Tables

To be determined from the approved domain relationships.

Potential association tables include:

- `brand_partners`
- `initiative_items`
- `initiative_partners`
- `initiative_sourcing_trips`
- `initiative_observations`
- `initiative_decisions`
- `initiative_purchase_orders`
- `initiative_inbound_shipments`
- `initiative_inventory_locations`
- `sourcing_trip_partners`
- `sourcing_trip_items`
- `observation_items`
- `observation_partners`
- `observation_purchase_orders`
- `decision_items`
- `decision_partners`
- `decision_purchase_orders`

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

---

## Status Values

Status values must be defined before SQLAlchemy implementation.

Potential status groups:

- Purchase order status
- Inbound shipment status
- Initiative status
- Decision status
- Item status
- Partner status
- Inventory movement type
- Inventory location status

---

## Deletion Strategy

Determine which records may be:

- hard deleted
- archived
- deactivated
- preserved permanently for historical integrity

Operational records such as purchase orders, inbound shipments, inventory_movements, observations, and decisions should generally remain part of the historical record.

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