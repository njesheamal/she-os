from sqlalchemy import Column, ForeignKey, Table, Uuid

from app.database.base import Base


def assoc(name, left_col, left_table, right_col, right_table):
    """Build a pure many-to-many association table.

    Composite PK of both FKs, no own `id`, no timestamps, no lifecycle.
    The PK indexes (left, right) leading with left; index=True on the
    right column covers the reverse lookup.
    """
    return Table(
        name,
        Base.metadata,
        Column(left_col, Uuid, ForeignKey(f"{left_table}.id"), primary_key=True),
        Column(
            right_col,
            Uuid,
            ForeignKey(f"{right_table}.id"),
            primary_key=True,
            index=True,
        ),
    )


# --- Brand ---
brand_initiatives = assoc("brand_initiatives", "brand_id", "brands", "initiative_id", "initiatives")
brand_items = assoc("brand_items", "brand_id", "brands", "item_id", "items")
brand_partners = assoc("brand_partners", "brand_id", "brands", "partner_id", "partners")
brand_sourcing_trips = assoc("brand_sourcing_trips", "brand_id", "brands", "sourcing_trip_id", "sourcing_trips")
brand_observations = assoc("brand_observations", "brand_id", "brands", "observation_id", "observations")
brand_decisions = assoc("brand_decisions", "brand_id", "brands", "decision_id", "decisions")
brand_purchase_orders = assoc("brand_purchase_orders", "brand_id", "brands", "purchase_order_id", "purchase_orders")
brand_inbound_shipments = assoc("brand_inbound_shipments", "brand_id", "brands", "inbound_shipment_id", "inbound_shipments")
brand_inventory_locations = assoc("brand_inventory_locations", "brand_id", "brands", "inventory_location_id", "inventory_locations")

# --- Initiative ---
initiative_items = assoc("initiative_items", "initiative_id", "initiatives", "item_id", "items")
initiative_partners = assoc("initiative_partners", "initiative_id", "initiatives", "partner_id", "partners")
initiative_sourcing_trips = assoc("initiative_sourcing_trips", "initiative_id", "initiatives", "sourcing_trip_id", "sourcing_trips")
initiative_observations = assoc("initiative_observations", "initiative_id", "initiatives", "observation_id", "observations")
initiative_decisions = assoc("initiative_decisions", "initiative_id", "initiatives", "decision_id", "decisions")
initiative_purchase_orders = assoc("initiative_purchase_orders", "initiative_id", "initiatives", "purchase_order_id", "purchase_orders")
initiative_inbound_shipments = assoc("initiative_inbound_shipments", "initiative_id", "initiatives", "inbound_shipment_id", "inbound_shipments")
initiative_inventory_locations = assoc("initiative_inventory_locations", "initiative_id", "initiatives", "inventory_location_id", "inventory_locations")

# --- Sourcing Trip ---
sourcing_trip_items = assoc("sourcing_trip_items", "sourcing_trip_id", "sourcing_trips", "item_id", "items")
sourcing_trip_partners = assoc("sourcing_trip_partners", "sourcing_trip_id", "sourcing_trips", "partner_id", "partners")
sourcing_trip_observations = assoc("sourcing_trip_observations", "sourcing_trip_id", "sourcing_trips", "observation_id", "observations")
sourcing_trip_decisions = assoc("sourcing_trip_decisions", "sourcing_trip_id", "sourcing_trips", "decision_id", "decisions")
sourcing_trip_purchase_orders = assoc("sourcing_trip_purchase_orders", "sourcing_trip_id", "sourcing_trips", "purchase_order_id", "purchase_orders")
sourcing_trip_inbound_shipments = assoc("sourcing_trip_inbound_shipments", "sourcing_trip_id", "sourcing_trips", "inbound_shipment_id", "inbound_shipments")

# --- Observation ---
observation_decisions = assoc("observation_decisions", "observation_id", "observations", "decision_id", "decisions")
observation_items = assoc("observation_items", "observation_id", "observations", "item_id", "items")
observation_partners = assoc("observation_partners", "observation_id", "observations", "partner_id", "partners")
observation_purchase_orders = assoc("observation_purchase_orders", "observation_id", "observations", "purchase_order_id", "purchase_orders")
observation_inbound_shipments = assoc("observation_inbound_shipments", "observation_id", "observations", "inbound_shipment_id", "inbound_shipments")
observation_inventory_locations = assoc("observation_inventory_locations", "observation_id", "observations", "inventory_location_id", "inventory_locations")
observation_inventory_movements = assoc("observation_inventory_movements", "observation_id", "observations", "inventory_movement_id", "inventory_movements")

# --- Decision ---
decision_items = assoc("decision_items", "decision_id", "decisions", "item_id", "items")
decision_partners = assoc("decision_partners", "decision_id", "decisions", "partner_id", "partners")
decision_purchase_orders = assoc("decision_purchase_orders", "decision_id", "decisions", "purchase_order_id", "purchase_orders")
decision_inbound_shipments = assoc("decision_inbound_shipments", "decision_id", "decisions", "inbound_shipment_id", "inbound_shipments")
decision_inventory_locations = assoc("decision_inventory_locations", "decision_id", "decisions", "inventory_location_id", "inventory_locations")
decision_inventory_movements = assoc("decision_inventory_movements", "decision_id", "decisions", "inventory_movement_id", "inventory_movements")

# --- Item ---
item_partners = assoc("item_partners", "item_id", "items", "partner_id", "partners")
