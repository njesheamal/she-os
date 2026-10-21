--
-- PostgreSQL database dump
--

\restrict 8agZM3ifipFZ7MYwkrAeUbyT6L9Xce6Q7e9qAvVgmSI8Gus0XuMnagQRnfnYClZ

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 16.15 (Debian 16.15-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.sourcing_trip_purchase_orders DROP CONSTRAINT IF EXISTS fk_sourcing_trip_purchase_orders_sourcing_trip_id_sourc_906f;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_purchase_orders DROP CONSTRAINT IF EXISTS fk_sourcing_trip_purchase_orders_purchase_order_id_purc_2a23;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_partners DROP CONSTRAINT IF EXISTS fk_sourcing_trip_partners_sourcing_trip_id_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_partners DROP CONSTRAINT IF EXISTS fk_sourcing_trip_partners_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_observations DROP CONSTRAINT IF EXISTS fk_sourcing_trip_observations_sourcing_trip_id_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_observations DROP CONSTRAINT IF EXISTS fk_sourcing_trip_observations_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_items DROP CONSTRAINT IF EXISTS fk_sourcing_trip_items_sourcing_trip_id_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_items DROP CONSTRAINT IF EXISTS fk_sourcing_trip_items_item_id_items;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_inbound_shipments DROP CONSTRAINT IF EXISTS fk_sourcing_trip_inbound_shipments_sourcing_trip_id_sou_4690;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_inbound_shipments DROP CONSTRAINT IF EXISTS fk_sourcing_trip_inbound_shipments_inbound_shipment_id__84f8;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_decisions DROP CONSTRAINT IF EXISTS fk_sourcing_trip_decisions_sourcing_trip_id_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_decisions DROP CONSTRAINT IF EXISTS fk_sourcing_trip_decisions_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.purchase_orders DROP CONSTRAINT IF EXISTS fk_purchase_orders_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.purchase_order_lines DROP CONSTRAINT IF EXISTS fk_purchase_order_lines_unit_of_measure_id_units_of_measure;
ALTER TABLE IF EXISTS ONLY public.purchase_order_lines DROP CONSTRAINT IF EXISTS fk_purchase_order_lines_purchase_order_id_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.purchase_order_lines DROP CONSTRAINT IF EXISTS fk_purchase_order_lines_item_id_items;
ALTER TABLE IF EXISTS ONLY public.partners DROP CONSTRAINT IF EXISTS fk_partners_partner_type_id_partner_types;
ALTER TABLE IF EXISTS ONLY public.observation_purchase_orders DROP CONSTRAINT IF EXISTS fk_observation_purchase_orders_purchase_order_id_purcha_5720;
ALTER TABLE IF EXISTS ONLY public.observation_purchase_orders DROP CONSTRAINT IF EXISTS fk_observation_purchase_orders_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_partners DROP CONSTRAINT IF EXISTS fk_observation_partners_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.observation_partners DROP CONSTRAINT IF EXISTS fk_observation_partners_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_items DROP CONSTRAINT IF EXISTS fk_observation_items_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_items DROP CONSTRAINT IF EXISTS fk_observation_items_item_id_items;
ALTER TABLE IF EXISTS ONLY public.observation_inventory_movements DROP CONSTRAINT IF EXISTS fk_observation_inventory_movements_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_inventory_movements DROP CONSTRAINT IF EXISTS fk_observation_inventory_movements_inventory_movement_i_754c;
ALTER TABLE IF EXISTS ONLY public.observation_inventory_locations DROP CONSTRAINT IF EXISTS fk_observation_inventory_locations_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_inventory_locations DROP CONSTRAINT IF EXISTS fk_observation_inventory_locations_inventory_location_i_db03;
ALTER TABLE IF EXISTS ONLY public.observation_inbound_shipments DROP CONSTRAINT IF EXISTS fk_observation_inbound_shipments_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_inbound_shipments DROP CONSTRAINT IF EXISTS fk_observation_inbound_shipments_inbound_shipment_id_in_0126;
ALTER TABLE IF EXISTS ONLY public.observation_decisions DROP CONSTRAINT IF EXISTS fk_observation_decisions_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.observation_decisions DROP CONSTRAINT IF EXISTS fk_observation_decisions_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.items DROP CONSTRAINT IF EXISTS fk_items_item_type_id_item_types;
ALTER TABLE IF EXISTS ONLY public.item_partners DROP CONSTRAINT IF EXISTS fk_item_partners_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.item_partners DROP CONSTRAINT IF EXISTS fk_item_partners_item_id_items;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS fk_inventory_movements_unit_of_measure_id_units_of_measure;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS fk_inventory_movements_related_movement_id_inventory_movements;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS fk_inventory_movements_item_id_items;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS fk_inventory_movements_inventory_movement_type_id_inven_6059;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS fk_inventory_movements_inventory_location_id_inventory__da53;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS fk_inventory_movements_inbound_shipment_line_id_inbound_d454;
ALTER TABLE IF EXISTS ONLY public.inventory_locations DROP CONSTRAINT IF EXISTS fk_inventory_locations_inventory_location_type_id_inven_927e;
ALTER TABLE IF EXISTS ONLY public.inventory_balances DROP CONSTRAINT IF EXISTS fk_inventory_balances_unit_of_measure_id_units_of_measure;
ALTER TABLE IF EXISTS ONLY public.inventory_balances DROP CONSTRAINT IF EXISTS fk_inventory_balances_item_id_items;
ALTER TABLE IF EXISTS ONLY public.inventory_balances DROP CONSTRAINT IF EXISTS fk_inventory_balances_inventory_location_id_inventory_locations;
ALTER TABLE IF EXISTS ONLY public.initiatives DROP CONSTRAINT IF EXISTS fk_initiatives_initiative_type_id_initiative_types;
ALTER TABLE IF EXISTS ONLY public.initiative_sourcing_trips DROP CONSTRAINT IF EXISTS fk_initiative_sourcing_trips_sourcing_trip_id_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.initiative_sourcing_trips DROP CONSTRAINT IF EXISTS fk_initiative_sourcing_trips_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_purchase_orders DROP CONSTRAINT IF EXISTS fk_initiative_purchase_orders_purchase_order_id_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.initiative_purchase_orders DROP CONSTRAINT IF EXISTS fk_initiative_purchase_orders_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_partners DROP CONSTRAINT IF EXISTS fk_initiative_partners_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.initiative_partners DROP CONSTRAINT IF EXISTS fk_initiative_partners_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_observations DROP CONSTRAINT IF EXISTS fk_initiative_observations_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.initiative_observations DROP CONSTRAINT IF EXISTS fk_initiative_observations_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_items DROP CONSTRAINT IF EXISTS fk_initiative_items_item_id_items;
ALTER TABLE IF EXISTS ONLY public.initiative_items DROP CONSTRAINT IF EXISTS fk_initiative_items_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_inventory_locations DROP CONSTRAINT IF EXISTS fk_initiative_inventory_locations_inventory_location_id_fda9;
ALTER TABLE IF EXISTS ONLY public.initiative_inventory_locations DROP CONSTRAINT IF EXISTS fk_initiative_inventory_locations_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_inbound_shipments DROP CONSTRAINT IF EXISTS fk_initiative_inbound_shipments_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_inbound_shipments DROP CONSTRAINT IF EXISTS fk_initiative_inbound_shipments_inbound_shipment_id_inb_790d;
ALTER TABLE IF EXISTS ONLY public.initiative_decisions DROP CONSTRAINT IF EXISTS fk_initiative_decisions_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_decisions DROP CONSTRAINT IF EXISTS fk_initiative_decisions_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.inbound_shipments DROP CONSTRAINT IF EXISTS fk_inbound_shipments_destination_inventory_location_id__9800;
ALTER TABLE IF EXISTS ONLY public.inbound_shipment_lines DROP CONSTRAINT IF EXISTS fk_inbound_shipment_lines_unit_of_measure_id_units_of_measure;
ALTER TABLE IF EXISTS ONLY public.inbound_shipment_lines DROP CONSTRAINT IF EXISTS fk_inbound_shipment_lines_purchase_order_line_id_purcha_c044;
ALTER TABLE IF EXISTS ONLY public.inbound_shipment_lines DROP CONSTRAINT IF EXISTS fk_inbound_shipment_lines_inbound_shipment_id_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.field_notes DROP CONSTRAINT IF EXISTS fk_field_notes_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.decision_purchase_orders DROP CONSTRAINT IF EXISTS fk_decision_purchase_orders_purchase_order_id_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.decision_purchase_orders DROP CONSTRAINT IF EXISTS fk_decision_purchase_orders_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.decision_partners DROP CONSTRAINT IF EXISTS fk_decision_partners_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.decision_partners DROP CONSTRAINT IF EXISTS fk_decision_partners_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.decision_items DROP CONSTRAINT IF EXISTS fk_decision_items_item_id_items;
ALTER TABLE IF EXISTS ONLY public.decision_items DROP CONSTRAINT IF EXISTS fk_decision_items_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.decision_inventory_movements DROP CONSTRAINT IF EXISTS fk_decision_inventory_movements_inventory_movement_id_i_7e1d;
ALTER TABLE IF EXISTS ONLY public.decision_inventory_movements DROP CONSTRAINT IF EXISTS fk_decision_inventory_movements_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.decision_inventory_locations DROP CONSTRAINT IF EXISTS fk_decision_inventory_locations_inventory_location_id_i_2ef5;
ALTER TABLE IF EXISTS ONLY public.decision_inventory_locations DROP CONSTRAINT IF EXISTS fk_decision_inventory_locations_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.decision_inbound_shipments DROP CONSTRAINT IF EXISTS fk_decision_inbound_shipments_inbound_shipment_id_inbou_776d;
ALTER TABLE IF EXISTS ONLY public.decision_inbound_shipments DROP CONSTRAINT IF EXISTS fk_decision_inbound_shipments_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.brand_sourcing_trips DROP CONSTRAINT IF EXISTS fk_brand_sourcing_trips_sourcing_trip_id_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.brand_sourcing_trips DROP CONSTRAINT IF EXISTS fk_brand_sourcing_trips_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_purchase_orders DROP CONSTRAINT IF EXISTS fk_brand_purchase_orders_purchase_order_id_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.brand_purchase_orders DROP CONSTRAINT IF EXISTS fk_brand_purchase_orders_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_partners DROP CONSTRAINT IF EXISTS fk_brand_partners_partner_id_partners;
ALTER TABLE IF EXISTS ONLY public.brand_partners DROP CONSTRAINT IF EXISTS fk_brand_partners_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_observations DROP CONSTRAINT IF EXISTS fk_brand_observations_observation_id_observations;
ALTER TABLE IF EXISTS ONLY public.brand_observations DROP CONSTRAINT IF EXISTS fk_brand_observations_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_items DROP CONSTRAINT IF EXISTS fk_brand_items_item_id_items;
ALTER TABLE IF EXISTS ONLY public.brand_items DROP CONSTRAINT IF EXISTS fk_brand_items_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_inventory_locations DROP CONSTRAINT IF EXISTS fk_brand_inventory_locations_inventory_location_id_inve_bf65;
ALTER TABLE IF EXISTS ONLY public.brand_inventory_locations DROP CONSTRAINT IF EXISTS fk_brand_inventory_locations_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_initiatives DROP CONSTRAINT IF EXISTS fk_brand_initiatives_initiative_id_initiatives;
ALTER TABLE IF EXISTS ONLY public.brand_initiatives DROP CONSTRAINT IF EXISTS fk_brand_initiatives_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_inbound_shipments DROP CONSTRAINT IF EXISTS fk_brand_inbound_shipments_inbound_shipment_id_inbound__1ef5;
ALTER TABLE IF EXISTS ONLY public.brand_inbound_shipments DROP CONSTRAINT IF EXISTS fk_brand_inbound_shipments_brand_id_brands;
ALTER TABLE IF EXISTS ONLY public.brand_decisions DROP CONSTRAINT IF EXISTS fk_brand_decisions_decision_id_decisions;
ALTER TABLE IF EXISTS ONLY public.brand_decisions DROP CONSTRAINT IF EXISTS fk_brand_decisions_brand_id_brands;
DROP INDEX IF EXISTS public.ix_units_of_measure_is_active;
DROP INDEX IF EXISTS public.ix_sourcing_trips_status;
DROP INDEX IF EXISTS public.ix_sourcing_trips_start_date;
DROP INDEX IF EXISTS public.ix_sourcing_trip_purchase_orders_purchase_order_id;
DROP INDEX IF EXISTS public.ix_sourcing_trip_partners_partner_id;
DROP INDEX IF EXISTS public.ix_sourcing_trip_observations_observation_id;
DROP INDEX IF EXISTS public.ix_sourcing_trip_items_item_id;
DROP INDEX IF EXISTS public.ix_sourcing_trip_inbound_shipments_inbound_shipment_id;
DROP INDEX IF EXISTS public.ix_sourcing_trip_decisions_decision_id;
DROP INDEX IF EXISTS public.ix_purchase_orders_status;
DROP INDEX IF EXISTS public.ix_purchase_orders_partner_id;
DROP INDEX IF EXISTS public.ix_purchase_orders_order_date;
DROP INDEX IF EXISTS public.ix_purchase_order_lines_purchase_order_id;
DROP INDEX IF EXISTS public.ix_purchase_order_lines_item_id;
DROP INDEX IF EXISTS public.ix_partners_status;
DROP INDEX IF EXISTS public.ix_partners_partner_type_id;
DROP INDEX IF EXISTS public.ix_partner_types_is_active;
DROP INDEX IF EXISTS public.ix_observations_observed_at;
DROP INDEX IF EXISTS public.ix_observation_purchase_orders_purchase_order_id;
DROP INDEX IF EXISTS public.ix_observation_partners_partner_id;
DROP INDEX IF EXISTS public.ix_observation_items_item_id;
DROP INDEX IF EXISTS public.ix_observation_inventory_movements_inventory_movement_id;
DROP INDEX IF EXISTS public.ix_observation_inventory_locations_inventory_location_id;
DROP INDEX IF EXISTS public.ix_observation_inbound_shipments_inbound_shipment_id;
DROP INDEX IF EXISTS public.ix_observation_decisions_decision_id;
DROP INDEX IF EXISTS public.ix_items_status;
DROP INDEX IF EXISTS public.ix_items_item_type_id;
DROP INDEX IF EXISTS public.ix_item_types_is_active;
DROP INDEX IF EXISTS public.ix_item_partners_partner_id;
DROP INDEX IF EXISTS public.ix_inventory_movements_occurred_at;
DROP INDEX IF EXISTS public.ix_inventory_movements_item_id;
DROP INDEX IF EXISTS public.ix_inventory_movements_inventory_movement_type_id;
DROP INDEX IF EXISTS public.ix_inventory_movements_inventory_location_id;
DROP INDEX IF EXISTS public.ix_inventory_movement_types_is_active;
DROP INDEX IF EXISTS public.ix_inventory_locations_status;
DROP INDEX IF EXISTS public.ix_inventory_locations_inventory_location_type_id;
DROP INDEX IF EXISTS public.ix_inventory_locations_country_code;
DROP INDEX IF EXISTS public.ix_inventory_locations_city;
DROP INDEX IF EXISTS public.ix_inventory_location_types_is_active;
DROP INDEX IF EXISTS public.ix_inventory_balances_item_id;
DROP INDEX IF EXISTS public.ix_inventory_balances_inventory_location_id;
DROP INDEX IF EXISTS public.ix_initiatives_status;
DROP INDEX IF EXISTS public.ix_initiatives_start_date;
DROP INDEX IF EXISTS public.ix_initiatives_initiative_type_id;
DROP INDEX IF EXISTS public.ix_initiative_types_is_active;
DROP INDEX IF EXISTS public.ix_initiative_sourcing_trips_sourcing_trip_id;
DROP INDEX IF EXISTS public.ix_initiative_purchase_orders_purchase_order_id;
DROP INDEX IF EXISTS public.ix_initiative_partners_partner_id;
DROP INDEX IF EXISTS public.ix_initiative_observations_observation_id;
DROP INDEX IF EXISTS public.ix_initiative_items_item_id;
DROP INDEX IF EXISTS public.ix_initiative_inventory_locations_inventory_location_id;
DROP INDEX IF EXISTS public.ix_initiative_inbound_shipments_inbound_shipment_id;
DROP INDEX IF EXISTS public.ix_initiative_decisions_decision_id;
DROP INDEX IF EXISTS public.ix_inbound_shipments_status;
DROP INDEX IF EXISTS public.ix_inbound_shipments_shipped_at;
DROP INDEX IF EXISTS public.ix_inbound_shipments_received_at;
DROP INDEX IF EXISTS public.ix_inbound_shipments_destination_inventory_location_id;
DROP INDEX IF EXISTS public.ix_inbound_shipment_lines_purchase_order_line_id;
DROP INDEX IF EXISTS public.ix_inbound_shipment_lines_inbound_shipment_id;
DROP INDEX IF EXISTS public.ix_field_notes_status;
DROP INDEX IF EXISTS public.ix_field_notes_slug;
DROP INDEX IF EXISTS public.ix_field_notes_published_at;
DROP INDEX IF EXISTS public.ix_field_notes_initiative_id;
DROP INDEX IF EXISTS public.ix_decisions_status;
DROP INDEX IF EXISTS public.ix_decisions_decided_at;
DROP INDEX IF EXISTS public.ix_decision_purchase_orders_purchase_order_id;
DROP INDEX IF EXISTS public.ix_decision_partners_partner_id;
DROP INDEX IF EXISTS public.ix_decision_items_item_id;
DROP INDEX IF EXISTS public.ix_decision_inventory_movements_inventory_movement_id;
DROP INDEX IF EXISTS public.ix_decision_inventory_locations_inventory_location_id;
DROP INDEX IF EXISTS public.ix_decision_inbound_shipments_inbound_shipment_id;
DROP INDEX IF EXISTS public.ix_brand_sourcing_trips_sourcing_trip_id;
DROP INDEX IF EXISTS public.ix_brand_purchase_orders_purchase_order_id;
DROP INDEX IF EXISTS public.ix_brand_partners_partner_id;
DROP INDEX IF EXISTS public.ix_brand_observations_observation_id;
DROP INDEX IF EXISTS public.ix_brand_items_item_id;
DROP INDEX IF EXISTS public.ix_brand_inventory_locations_inventory_location_id;
DROP INDEX IF EXISTS public.ix_brand_initiatives_initiative_id;
DROP INDEX IF EXISTS public.ix_brand_inbound_shipments_inbound_shipment_id;
DROP INDEX IF EXISTS public.ix_brand_decisions_decision_id;
ALTER TABLE IF EXISTS ONLY public.units_of_measure DROP CONSTRAINT IF EXISTS uq_units_of_measure_slug;
ALTER TABLE IF EXISTS ONLY public.units_of_measure DROP CONSTRAINT IF EXISTS uq_units_of_measure_name;
ALTER TABLE IF EXISTS ONLY public.sourcing_trips DROP CONSTRAINT IF EXISTS uq_sourcing_trips_slug;
ALTER TABLE IF EXISTS ONLY public.purchase_orders DROP CONSTRAINT IF EXISTS uq_purchase_orders_purchase_order_number;
ALTER TABLE IF EXISTS ONLY public.partners DROP CONSTRAINT IF EXISTS uq_partners_slug;
ALTER TABLE IF EXISTS ONLY public.partner_types DROP CONSTRAINT IF EXISTS uq_partner_types_slug;
ALTER TABLE IF EXISTS ONLY public.partner_types DROP CONSTRAINT IF EXISTS uq_partner_types_name;
ALTER TABLE IF EXISTS ONLY public.items DROP CONSTRAINT IF EXISTS uq_items_slug;
ALTER TABLE IF EXISTS ONLY public.items DROP CONSTRAINT IF EXISTS uq_items_sku;
ALTER TABLE IF EXISTS ONLY public.item_types DROP CONSTRAINT IF EXISTS uq_item_types_slug;
ALTER TABLE IF EXISTS ONLY public.item_types DROP CONSTRAINT IF EXISTS uq_item_types_name;
ALTER TABLE IF EXISTS ONLY public.inventory_movement_types DROP CONSTRAINT IF EXISTS uq_inventory_movement_types_slug;
ALTER TABLE IF EXISTS ONLY public.inventory_movement_types DROP CONSTRAINT IF EXISTS uq_inventory_movement_types_name;
ALTER TABLE IF EXISTS ONLY public.inventory_locations DROP CONSTRAINT IF EXISTS uq_inventory_locations_slug;
ALTER TABLE IF EXISTS ONLY public.inventory_location_types DROP CONSTRAINT IF EXISTS uq_inventory_location_types_slug;
ALTER TABLE IF EXISTS ONLY public.inventory_location_types DROP CONSTRAINT IF EXISTS uq_inventory_location_types_name;
ALTER TABLE IF EXISTS ONLY public.initiatives DROP CONSTRAINT IF EXISTS uq_initiatives_slug;
ALTER TABLE IF EXISTS ONLY public.initiative_types DROP CONSTRAINT IF EXISTS uq_initiative_types_slug;
ALTER TABLE IF EXISTS ONLY public.initiative_types DROP CONSTRAINT IF EXISTS uq_initiative_types_name;
ALTER TABLE IF EXISTS ONLY public.inbound_shipments DROP CONSTRAINT IF EXISTS uq_inbound_shipments_inbound_shipment_number;
ALTER TABLE IF EXISTS ONLY public.brands DROP CONSTRAINT IF EXISTS uq_brands_slug;
ALTER TABLE IF EXISTS ONLY public.brands DROP CONSTRAINT IF EXISTS uq_brands_name;
ALTER TABLE IF EXISTS ONLY public.inbound_shipment_lines DROP CONSTRAINT IF EXISTS shipment_po_line_unique;
ALTER TABLE IF EXISTS ONLY public.purchase_order_lines DROP CONSTRAINT IF EXISTS po_line_number_unique;
ALTER TABLE IF EXISTS ONLY public.units_of_measure DROP CONSTRAINT IF EXISTS pk_units_of_measure;
ALTER TABLE IF EXISTS ONLY public.sourcing_trips DROP CONSTRAINT IF EXISTS pk_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_purchase_orders DROP CONSTRAINT IF EXISTS pk_sourcing_trip_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_partners DROP CONSTRAINT IF EXISTS pk_sourcing_trip_partners;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_observations DROP CONSTRAINT IF EXISTS pk_sourcing_trip_observations;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_items DROP CONSTRAINT IF EXISTS pk_sourcing_trip_items;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_inbound_shipments DROP CONSTRAINT IF EXISTS pk_sourcing_trip_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.sourcing_trip_decisions DROP CONSTRAINT IF EXISTS pk_sourcing_trip_decisions;
ALTER TABLE IF EXISTS ONLY public.purchase_orders DROP CONSTRAINT IF EXISTS pk_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.purchase_order_lines DROP CONSTRAINT IF EXISTS pk_purchase_order_lines;
ALTER TABLE IF EXISTS ONLY public.partners DROP CONSTRAINT IF EXISTS pk_partners;
ALTER TABLE IF EXISTS ONLY public.partner_types DROP CONSTRAINT IF EXISTS pk_partner_types;
ALTER TABLE IF EXISTS ONLY public.observations DROP CONSTRAINT IF EXISTS pk_observations;
ALTER TABLE IF EXISTS ONLY public.observation_purchase_orders DROP CONSTRAINT IF EXISTS pk_observation_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.observation_partners DROP CONSTRAINT IF EXISTS pk_observation_partners;
ALTER TABLE IF EXISTS ONLY public.observation_items DROP CONSTRAINT IF EXISTS pk_observation_items;
ALTER TABLE IF EXISTS ONLY public.observation_inventory_movements DROP CONSTRAINT IF EXISTS pk_observation_inventory_movements;
ALTER TABLE IF EXISTS ONLY public.observation_inventory_locations DROP CONSTRAINT IF EXISTS pk_observation_inventory_locations;
ALTER TABLE IF EXISTS ONLY public.observation_inbound_shipments DROP CONSTRAINT IF EXISTS pk_observation_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.observation_decisions DROP CONSTRAINT IF EXISTS pk_observation_decisions;
ALTER TABLE IF EXISTS ONLY public.items DROP CONSTRAINT IF EXISTS pk_items;
ALTER TABLE IF EXISTS ONLY public.item_types DROP CONSTRAINT IF EXISTS pk_item_types;
ALTER TABLE IF EXISTS ONLY public.item_partners DROP CONSTRAINT IF EXISTS pk_item_partners;
ALTER TABLE IF EXISTS ONLY public.inventory_movements DROP CONSTRAINT IF EXISTS pk_inventory_movements;
ALTER TABLE IF EXISTS ONLY public.inventory_movement_types DROP CONSTRAINT IF EXISTS pk_inventory_movement_types;
ALTER TABLE IF EXISTS ONLY public.inventory_locations DROP CONSTRAINT IF EXISTS pk_inventory_locations;
ALTER TABLE IF EXISTS ONLY public.inventory_location_types DROP CONSTRAINT IF EXISTS pk_inventory_location_types;
ALTER TABLE IF EXISTS ONLY public.inventory_balances DROP CONSTRAINT IF EXISTS pk_inventory_balances;
ALTER TABLE IF EXISTS ONLY public.initiatives DROP CONSTRAINT IF EXISTS pk_initiatives;
ALTER TABLE IF EXISTS ONLY public.initiative_types DROP CONSTRAINT IF EXISTS pk_initiative_types;
ALTER TABLE IF EXISTS ONLY public.initiative_sourcing_trips DROP CONSTRAINT IF EXISTS pk_initiative_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.initiative_purchase_orders DROP CONSTRAINT IF EXISTS pk_initiative_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.initiative_partners DROP CONSTRAINT IF EXISTS pk_initiative_partners;
ALTER TABLE IF EXISTS ONLY public.initiative_observations DROP CONSTRAINT IF EXISTS pk_initiative_observations;
ALTER TABLE IF EXISTS ONLY public.initiative_items DROP CONSTRAINT IF EXISTS pk_initiative_items;
ALTER TABLE IF EXISTS ONLY public.initiative_inventory_locations DROP CONSTRAINT IF EXISTS pk_initiative_inventory_locations;
ALTER TABLE IF EXISTS ONLY public.initiative_inbound_shipments DROP CONSTRAINT IF EXISTS pk_initiative_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.initiative_decisions DROP CONSTRAINT IF EXISTS pk_initiative_decisions;
ALTER TABLE IF EXISTS ONLY public.inbound_shipments DROP CONSTRAINT IF EXISTS pk_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.inbound_shipment_lines DROP CONSTRAINT IF EXISTS pk_inbound_shipment_lines;
ALTER TABLE IF EXISTS ONLY public.field_notes DROP CONSTRAINT IF EXISTS pk_field_notes;
ALTER TABLE IF EXISTS ONLY public.decisions DROP CONSTRAINT IF EXISTS pk_decisions;
ALTER TABLE IF EXISTS ONLY public.decision_purchase_orders DROP CONSTRAINT IF EXISTS pk_decision_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.decision_partners DROP CONSTRAINT IF EXISTS pk_decision_partners;
ALTER TABLE IF EXISTS ONLY public.decision_items DROP CONSTRAINT IF EXISTS pk_decision_items;
ALTER TABLE IF EXISTS ONLY public.decision_inventory_movements DROP CONSTRAINT IF EXISTS pk_decision_inventory_movements;
ALTER TABLE IF EXISTS ONLY public.decision_inventory_locations DROP CONSTRAINT IF EXISTS pk_decision_inventory_locations;
ALTER TABLE IF EXISTS ONLY public.decision_inbound_shipments DROP CONSTRAINT IF EXISTS pk_decision_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.brands DROP CONSTRAINT IF EXISTS pk_brands;
ALTER TABLE IF EXISTS ONLY public.brand_sourcing_trips DROP CONSTRAINT IF EXISTS pk_brand_sourcing_trips;
ALTER TABLE IF EXISTS ONLY public.brand_purchase_orders DROP CONSTRAINT IF EXISTS pk_brand_purchase_orders;
ALTER TABLE IF EXISTS ONLY public.brand_partners DROP CONSTRAINT IF EXISTS pk_brand_partners;
ALTER TABLE IF EXISTS ONLY public.brand_observations DROP CONSTRAINT IF EXISTS pk_brand_observations;
ALTER TABLE IF EXISTS ONLY public.brand_items DROP CONSTRAINT IF EXISTS pk_brand_items;
ALTER TABLE IF EXISTS ONLY public.brand_inventory_locations DROP CONSTRAINT IF EXISTS pk_brand_inventory_locations;
ALTER TABLE IF EXISTS ONLY public.brand_initiatives DROP CONSTRAINT IF EXISTS pk_brand_initiatives;
ALTER TABLE IF EXISTS ONLY public.brand_inbound_shipments DROP CONSTRAINT IF EXISTS pk_brand_inbound_shipments;
ALTER TABLE IF EXISTS ONLY public.brand_decisions DROP CONSTRAINT IF EXISTS pk_brand_decisions;
ALTER TABLE IF EXISTS ONLY public.inventory_balances DROP CONSTRAINT IF EXISTS item_location_unique;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
DROP TABLE IF EXISTS public.units_of_measure;
DROP TABLE IF EXISTS public.sourcing_trips;
DROP TABLE IF EXISTS public.sourcing_trip_purchase_orders;
DROP TABLE IF EXISTS public.sourcing_trip_partners;
DROP TABLE IF EXISTS public.sourcing_trip_observations;
DROP TABLE IF EXISTS public.sourcing_trip_items;
DROP TABLE IF EXISTS public.sourcing_trip_inbound_shipments;
DROP TABLE IF EXISTS public.sourcing_trip_decisions;
DROP TABLE IF EXISTS public.purchase_orders;
DROP TABLE IF EXISTS public.purchase_order_lines;
DROP TABLE IF EXISTS public.partners;
DROP TABLE IF EXISTS public.partner_types;
DROP TABLE IF EXISTS public.observations;
DROP TABLE IF EXISTS public.observation_purchase_orders;
DROP TABLE IF EXISTS public.observation_partners;
DROP TABLE IF EXISTS public.observation_items;
DROP TABLE IF EXISTS public.observation_inventory_movements;
DROP TABLE IF EXISTS public.observation_inventory_locations;
DROP TABLE IF EXISTS public.observation_inbound_shipments;
DROP TABLE IF EXISTS public.observation_decisions;
DROP TABLE IF EXISTS public.items;
DROP TABLE IF EXISTS public.item_types;
DROP TABLE IF EXISTS public.item_partners;
DROP TABLE IF EXISTS public.inventory_movements;
DROP TABLE IF EXISTS public.inventory_movement_types;
DROP TABLE IF EXISTS public.inventory_locations;
DROP TABLE IF EXISTS public.inventory_location_types;
DROP TABLE IF EXISTS public.inventory_balances;
DROP TABLE IF EXISTS public.initiatives;
DROP TABLE IF EXISTS public.initiative_types;
DROP TABLE IF EXISTS public.initiative_sourcing_trips;
DROP TABLE IF EXISTS public.initiative_purchase_orders;
DROP TABLE IF EXISTS public.initiative_partners;
DROP TABLE IF EXISTS public.initiative_observations;
DROP TABLE IF EXISTS public.initiative_items;
DROP TABLE IF EXISTS public.initiative_inventory_locations;
DROP TABLE IF EXISTS public.initiative_inbound_shipments;
DROP TABLE IF EXISTS public.initiative_decisions;
DROP TABLE IF EXISTS public.inbound_shipments;
DROP TABLE IF EXISTS public.inbound_shipment_lines;
DROP TABLE IF EXISTS public.field_notes;
DROP TABLE IF EXISTS public.decisions;
DROP TABLE IF EXISTS public.decision_purchase_orders;
DROP TABLE IF EXISTS public.decision_partners;
DROP TABLE IF EXISTS public.decision_items;
DROP TABLE IF EXISTS public.decision_inventory_movements;
DROP TABLE IF EXISTS public.decision_inventory_locations;
DROP TABLE IF EXISTS public.decision_inbound_shipments;
DROP TABLE IF EXISTS public.brands;
DROP TABLE IF EXISTS public.brand_sourcing_trips;
DROP TABLE IF EXISTS public.brand_purchase_orders;
DROP TABLE IF EXISTS public.brand_partners;
DROP TABLE IF EXISTS public.brand_observations;
DROP TABLE IF EXISTS public.brand_items;
DROP TABLE IF EXISTS public.brand_inventory_locations;
DROP TABLE IF EXISTS public.brand_initiatives;
DROP TABLE IF EXISTS public.brand_inbound_shipments;
DROP TABLE IF EXISTS public.brand_decisions;
DROP TABLE IF EXISTS public.alembic_version;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO she_os_user;

--
-- Name: brand_decisions; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_decisions (
    brand_id uuid NOT NULL,
    decision_id uuid NOT NULL
);


ALTER TABLE public.brand_decisions OWNER TO she_os_user;

--
-- Name: brand_inbound_shipments; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_inbound_shipments (
    brand_id uuid NOT NULL,
    inbound_shipment_id uuid NOT NULL
);


ALTER TABLE public.brand_inbound_shipments OWNER TO she_os_user;

--
-- Name: brand_initiatives; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_initiatives (
    brand_id uuid NOT NULL,
    initiative_id uuid NOT NULL
);


ALTER TABLE public.brand_initiatives OWNER TO she_os_user;

--
-- Name: brand_inventory_locations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_inventory_locations (
    brand_id uuid NOT NULL,
    inventory_location_id uuid NOT NULL
);


ALTER TABLE public.brand_inventory_locations OWNER TO she_os_user;

--
-- Name: brand_items; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_items (
    brand_id uuid NOT NULL,
    item_id uuid NOT NULL
);


ALTER TABLE public.brand_items OWNER TO she_os_user;

--
-- Name: brand_observations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_observations (
    brand_id uuid NOT NULL,
    observation_id uuid NOT NULL
);


ALTER TABLE public.brand_observations OWNER TO she_os_user;

--
-- Name: brand_partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_partners (
    brand_id uuid NOT NULL,
    partner_id uuid NOT NULL
);


ALTER TABLE public.brand_partners OWNER TO she_os_user;

--
-- Name: brand_purchase_orders; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_purchase_orders (
    brand_id uuid NOT NULL,
    purchase_order_id uuid NOT NULL
);


ALTER TABLE public.brand_purchase_orders OWNER TO she_os_user;

--
-- Name: brand_sourcing_trips; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brand_sourcing_trips (
    brand_id uuid NOT NULL,
    sourcing_trip_id uuid NOT NULL
);


ALTER TABLE public.brand_sourcing_trips OWNER TO she_os_user;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.brands (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_brands_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_brands_slug_not_empty CHECK (((slug)::text <> ''::text)),
    CONSTRAINT ck_brands_status_valid CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.brands OWNER TO she_os_user;

--
-- Name: decision_inbound_shipments; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decision_inbound_shipments (
    decision_id uuid NOT NULL,
    inbound_shipment_id uuid NOT NULL
);


ALTER TABLE public.decision_inbound_shipments OWNER TO she_os_user;

--
-- Name: decision_inventory_locations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decision_inventory_locations (
    decision_id uuid NOT NULL,
    inventory_location_id uuid NOT NULL
);


ALTER TABLE public.decision_inventory_locations OWNER TO she_os_user;

--
-- Name: decision_inventory_movements; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decision_inventory_movements (
    decision_id uuid NOT NULL,
    inventory_movement_id uuid NOT NULL
);


ALTER TABLE public.decision_inventory_movements OWNER TO she_os_user;

--
-- Name: decision_items; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decision_items (
    decision_id uuid NOT NULL,
    item_id uuid NOT NULL
);


ALTER TABLE public.decision_items OWNER TO she_os_user;

--
-- Name: decision_partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decision_partners (
    decision_id uuid NOT NULL,
    partner_id uuid NOT NULL
);


ALTER TABLE public.decision_partners OWNER TO she_os_user;

--
-- Name: decision_purchase_orders; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decision_purchase_orders (
    decision_id uuid NOT NULL,
    purchase_order_id uuid NOT NULL
);


ALTER TABLE public.decision_purchase_orders OWNER TO she_os_user;

--
-- Name: decisions; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.decisions (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    decision_summary text NOT NULL,
    reasoning text,
    status character varying(20) NOT NULL,
    decided_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_decisions_status_valid CHECK (((status)::text = ANY ((ARRAY['proposed'::character varying, 'approved'::character varying, 'in_effect'::character varying, 'superseded'::character varying, 'archived'::character varying])::text[]))),
    CONSTRAINT ck_decisions_summary_not_empty CHECK ((decision_summary <> ''::text)),
    CONSTRAINT ck_decisions_title_not_empty CHECK (((title)::text <> ''::text))
);


ALTER TABLE public.decisions OWNER TO she_os_user;

--
-- Name: field_notes; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.field_notes (
    id uuid NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    status character varying(20) NOT NULL,
    theme character varying(255),
    poem text NOT NULL,
    media jsonb,
    essay text,
    excerpt character varying(500),
    initiative_id uuid,
    published_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    sources jsonb,
    tags jsonb,
    CONSTRAINT ck_field_notes_poem_not_empty CHECK ((poem <> ''::text)),
    CONSTRAINT ck_field_notes_status_valid CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'published'::character varying])::text[]))),
    CONSTRAINT ck_field_notes_title_not_empty CHECK (((title)::text <> ''::text))
);


ALTER TABLE public.field_notes OWNER TO she_os_user;

--
-- Name: inbound_shipment_lines; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inbound_shipment_lines (
    id uuid NOT NULL,
    inbound_shipment_id uuid NOT NULL,
    purchase_order_line_id uuid NOT NULL,
    quantity_shipped numeric(14,4) NOT NULL,
    quantity_received numeric(14,4),
    quantity_accepted numeric(14,4),
    quantity_damaged numeric(14,4),
    unit_of_measure_id uuid NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inbound_shipment_lines_quantity_accepted_non_negative CHECK ((quantity_accepted >= (0)::numeric)),
    CONSTRAINT ck_inbound_shipment_lines_quantity_damaged_non_negative CHECK ((quantity_damaged >= (0)::numeric)),
    CONSTRAINT ck_inbound_shipment_lines_quantity_received_non_negative CHECK ((quantity_received >= (0)::numeric)),
    CONSTRAINT ck_inbound_shipment_lines_quantity_shipped_non_negative CHECK ((quantity_shipped >= (0)::numeric))
);


ALTER TABLE public.inbound_shipment_lines OWNER TO she_os_user;

--
-- Name: inbound_shipments; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inbound_shipments (
    id uuid NOT NULL,
    inbound_shipment_number character varying(50) NOT NULL,
    status character varying(20) NOT NULL,
    tracking_number character varying(100),
    carrier_name character varying(100),
    destination_inventory_location_id uuid,
    shipped_at timestamp with time zone,
    received_at timestamp with time zone,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inbound_shipments_dates_ordered CHECK ((received_at >= shipped_at)),
    CONSTRAINT ck_inbound_shipments_number_not_empty CHECK (((inbound_shipment_number)::text <> ''::text)),
    CONSTRAINT ck_inbound_shipments_status_valid CHECK (((status)::text = ANY ((ARRAY['preparing'::character varying, 'in_transit'::character varying, 'partially_received'::character varying, 'received'::character varying, 'closed'::character varying])::text[])))
);


ALTER TABLE public.inbound_shipments OWNER TO she_os_user;

--
-- Name: initiative_decisions; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_decisions (
    initiative_id uuid NOT NULL,
    decision_id uuid NOT NULL
);


ALTER TABLE public.initiative_decisions OWNER TO she_os_user;

--
-- Name: initiative_inbound_shipments; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_inbound_shipments (
    initiative_id uuid NOT NULL,
    inbound_shipment_id uuid NOT NULL
);


ALTER TABLE public.initiative_inbound_shipments OWNER TO she_os_user;

--
-- Name: initiative_inventory_locations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_inventory_locations (
    initiative_id uuid NOT NULL,
    inventory_location_id uuid NOT NULL
);


ALTER TABLE public.initiative_inventory_locations OWNER TO she_os_user;

--
-- Name: initiative_items; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_items (
    initiative_id uuid NOT NULL,
    item_id uuid NOT NULL
);


ALTER TABLE public.initiative_items OWNER TO she_os_user;

--
-- Name: initiative_observations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_observations (
    initiative_id uuid NOT NULL,
    observation_id uuid NOT NULL
);


ALTER TABLE public.initiative_observations OWNER TO she_os_user;

--
-- Name: initiative_partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_partners (
    initiative_id uuid NOT NULL,
    partner_id uuid NOT NULL
);


ALTER TABLE public.initiative_partners OWNER TO she_os_user;

--
-- Name: initiative_purchase_orders; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_purchase_orders (
    initiative_id uuid NOT NULL,
    purchase_order_id uuid NOT NULL
);


ALTER TABLE public.initiative_purchase_orders OWNER TO she_os_user;

--
-- Name: initiative_sourcing_trips; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_sourcing_trips (
    initiative_id uuid NOT NULL,
    sourcing_trip_id uuid NOT NULL
);


ALTER TABLE public.initiative_sourcing_trips OWNER TO she_os_user;

--
-- Name: initiative_types; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiative_types (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_initiative_types_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_initiative_types_slug_not_empty CHECK (((slug)::text <> ''::text))
);


ALTER TABLE public.initiative_types OWNER TO she_os_user;

--
-- Name: initiatives; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.initiatives (
    id uuid NOT NULL,
    initiative_type_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    start_date date,
    end_date date,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_initiatives_dates_ordered CHECK ((end_date >= start_date)),
    CONSTRAINT ck_initiatives_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_initiatives_slug_not_empty CHECK (((slug)::text <> ''::text)),
    CONSTRAINT ck_initiatives_status_valid CHECK (((status)::text = ANY ((ARRAY['planned'::character varying, 'active'::character varying, 'on_hold'::character varying, 'completed'::character varying, 'cancelled'::character varying])::text[])))
);


ALTER TABLE public.initiatives OWNER TO she_os_user;

--
-- Name: inventory_balances; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inventory_balances (
    id uuid NOT NULL,
    item_id uuid NOT NULL,
    inventory_location_id uuid NOT NULL,
    quantity_on_hand numeric(14,4) NOT NULL,
    unit_of_measure_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inventory_balances_quantity_on_hand_non_negative CHECK ((quantity_on_hand >= (0)::numeric))
);


ALTER TABLE public.inventory_balances OWNER TO she_os_user;

--
-- Name: inventory_location_types; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inventory_location_types (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inventory_location_types_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_inventory_location_types_slug_not_empty CHECK (((slug)::text <> ''::text))
);


ALTER TABLE public.inventory_location_types OWNER TO she_os_user;

--
-- Name: inventory_locations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inventory_locations (
    id uuid NOT NULL,
    inventory_location_type_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    address_line_1 character varying(255),
    address_line_2 character varying(255),
    city character varying(100),
    region character varying(100),
    postal_code character varying(20),
    country_code character(2),
    active_from timestamp with time zone,
    active_until timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inventory_locations_active_dates_ordered CHECK ((active_until >= active_from)),
    CONSTRAINT ck_inventory_locations_country_code_valid CHECK ((country_code ~ '^[A-Z]{2}$'::text)),
    CONSTRAINT ck_inventory_locations_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_inventory_locations_slug_not_empty CHECK (((slug)::text <> ''::text)),
    CONSTRAINT ck_inventory_locations_status_valid CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.inventory_locations OWNER TO she_os_user;

--
-- Name: inventory_movement_types; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inventory_movement_types (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inventory_movement_types_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_inventory_movement_types_slug_not_empty CHECK (((slug)::text <> ''::text))
);


ALTER TABLE public.inventory_movement_types OWNER TO she_os_user;

--
-- Name: inventory_movements; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.inventory_movements (
    id uuid NOT NULL,
    item_id uuid NOT NULL,
    inventory_location_id uuid NOT NULL,
    inventory_movement_type_id uuid NOT NULL,
    inbound_shipment_line_id uuid,
    related_movement_id uuid,
    quantity_delta numeric(14,4) NOT NULL,
    unit_of_measure_id uuid NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_inventory_movements_quantity_delta_non_zero CHECK ((quantity_delta <> (0)::numeric))
);


ALTER TABLE public.inventory_movements OWNER TO she_os_user;

--
-- Name: item_partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.item_partners (
    item_id uuid NOT NULL,
    partner_id uuid NOT NULL
);


ALTER TABLE public.item_partners OWNER TO she_os_user;

--
-- Name: item_types; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.item_types (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_item_types_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_item_types_slug_not_empty CHECK (((slug)::text <> ''::text))
);


ALTER TABLE public.item_types OWNER TO she_os_user;

--
-- Name: items; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.items (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    sku character varying(100),
    item_type_id uuid NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_items_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_items_sku_not_empty CHECK (((sku)::text <> ''::text)),
    CONSTRAINT ck_items_slug_not_empty CHECK (((slug)::text <> ''::text)),
    CONSTRAINT ck_items_status_valid CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'discontinued'::character varying])::text[])))
);


ALTER TABLE public.items OWNER TO she_os_user;

--
-- Name: observation_decisions; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_decisions (
    observation_id uuid NOT NULL,
    decision_id uuid NOT NULL
);


ALTER TABLE public.observation_decisions OWNER TO she_os_user;

--
-- Name: observation_inbound_shipments; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_inbound_shipments (
    observation_id uuid NOT NULL,
    inbound_shipment_id uuid NOT NULL
);


ALTER TABLE public.observation_inbound_shipments OWNER TO she_os_user;

--
-- Name: observation_inventory_locations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_inventory_locations (
    observation_id uuid NOT NULL,
    inventory_location_id uuid NOT NULL
);


ALTER TABLE public.observation_inventory_locations OWNER TO she_os_user;

--
-- Name: observation_inventory_movements; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_inventory_movements (
    observation_id uuid NOT NULL,
    inventory_movement_id uuid NOT NULL
);


ALTER TABLE public.observation_inventory_movements OWNER TO she_os_user;

--
-- Name: observation_items; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_items (
    observation_id uuid NOT NULL,
    item_id uuid NOT NULL
);


ALTER TABLE public.observation_items OWNER TO she_os_user;

--
-- Name: observation_partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_partners (
    observation_id uuid NOT NULL,
    partner_id uuid NOT NULL
);


ALTER TABLE public.observation_partners OWNER TO she_os_user;

--
-- Name: observation_purchase_orders; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observation_purchase_orders (
    observation_id uuid NOT NULL,
    purchase_order_id uuid NOT NULL
);


ALTER TABLE public.observation_purchase_orders OWNER TO she_os_user;

--
-- Name: observations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.observations (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    details text NOT NULL,
    observed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_observations_details_not_empty CHECK ((details <> ''::text)),
    CONSTRAINT ck_observations_title_not_empty CHECK (((title)::text <> ''::text))
);


ALTER TABLE public.observations OWNER TO she_os_user;

--
-- Name: partner_types; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.partner_types (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_partner_types_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_partner_types_slug_not_empty CHECK (((slug)::text <> ''::text))
);


ALTER TABLE public.partner_types OWNER TO she_os_user;

--
-- Name: partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.partners (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    partner_type_id uuid NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    website character varying(255),
    email character varying(255),
    phone character varying(50),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_partners_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_partners_slug_not_empty CHECK (((slug)::text <> ''::text)),
    CONSTRAINT ck_partners_status_valid CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.partners OWNER TO she_os_user;

--
-- Name: purchase_order_lines; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.purchase_order_lines (
    id uuid NOT NULL,
    purchase_order_id uuid NOT NULL,
    item_id uuid NOT NULL,
    line_number integer NOT NULL,
    description text,
    quantity_ordered numeric(14,4) NOT NULL,
    unit_of_measure_id uuid NOT NULL,
    unit_price numeric(14,4),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_purchase_order_lines_line_number_positive CHECK ((line_number > 0)),
    CONSTRAINT ck_purchase_order_lines_quantity_ordered_non_negative CHECK ((quantity_ordered >= (0)::numeric)),
    CONSTRAINT ck_purchase_order_lines_unit_price_non_negative CHECK ((unit_price >= (0)::numeric))
);


ALTER TABLE public.purchase_order_lines OWNER TO she_os_user;

--
-- Name: purchase_orders; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.purchase_orders (
    id uuid NOT NULL,
    purchase_order_number character varying(50) NOT NULL,
    partner_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    order_date date NOT NULL,
    expected_date date,
    currency_code character(3),
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    production_brief text,
    CONSTRAINT ck_purchase_orders_currency_code_valid CHECK ((currency_code ~ '^[A-Z]{3}$'::text)),
    CONSTRAINT ck_purchase_orders_dates_ordered CHECK ((expected_date >= order_date)),
    CONSTRAINT ck_purchase_orders_number_not_empty CHECK (((purchase_order_number)::text <> ''::text)),
    CONSTRAINT ck_purchase_orders_status_valid CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'submitted'::character varying, 'accepted'::character varying, 'in_production'::character varying, 'partially_fulfilled'::character varying, 'fulfilled'::character varying, 'cancelled'::character varying])::text[])))
);


ALTER TABLE public.purchase_orders OWNER TO she_os_user;

--
-- Name: sourcing_trip_decisions; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trip_decisions (
    sourcing_trip_id uuid NOT NULL,
    decision_id uuid NOT NULL
);


ALTER TABLE public.sourcing_trip_decisions OWNER TO she_os_user;

--
-- Name: sourcing_trip_inbound_shipments; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trip_inbound_shipments (
    sourcing_trip_id uuid NOT NULL,
    inbound_shipment_id uuid NOT NULL
);


ALTER TABLE public.sourcing_trip_inbound_shipments OWNER TO she_os_user;

--
-- Name: sourcing_trip_items; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trip_items (
    sourcing_trip_id uuid NOT NULL,
    item_id uuid NOT NULL
);


ALTER TABLE public.sourcing_trip_items OWNER TO she_os_user;

--
-- Name: sourcing_trip_observations; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trip_observations (
    sourcing_trip_id uuid NOT NULL,
    observation_id uuid NOT NULL
);


ALTER TABLE public.sourcing_trip_observations OWNER TO she_os_user;

--
-- Name: sourcing_trip_partners; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trip_partners (
    sourcing_trip_id uuid NOT NULL,
    partner_id uuid NOT NULL
);


ALTER TABLE public.sourcing_trip_partners OWNER TO she_os_user;

--
-- Name: sourcing_trip_purchase_orders; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trip_purchase_orders (
    sourcing_trip_id uuid NOT NULL,
    purchase_order_id uuid NOT NULL
);


ALTER TABLE public.sourcing_trip_purchase_orders OWNER TO she_os_user;

--
-- Name: sourcing_trips; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.sourcing_trips (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    start_date date,
    end_date date,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_sourcing_trips_dates_ordered CHECK ((end_date >= start_date)),
    CONSTRAINT ck_sourcing_trips_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_sourcing_trips_slug_not_empty CHECK (((slug)::text <> ''::text)),
    CONSTRAINT ck_sourcing_trips_status_valid CHECK (((status)::text = ANY ((ARRAY['planned'::character varying, 'in_progress'::character varying, 'completed'::character varying, 'cancelled'::character varying])::text[])))
);


ALTER TABLE public.sourcing_trips OWNER TO she_os_user;

--
-- Name: units_of_measure; Type: TABLE; Schema: public; Owner: she_os_user
--

CREATE TABLE public.units_of_measure (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_units_of_measure_name_not_empty CHECK (((name)::text <> ''::text)),
    CONSTRAINT ck_units_of_measure_slug_not_empty CHECK (((slug)::text <> ''::text))
);


ALTER TABLE public.units_of_measure OWNER TO she_os_user;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.alembic_version (version_num) FROM stdin;
a31694329048
\.


--
-- Data for Name: brand_decisions; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_decisions (brand_id, decision_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	14a51e18-4fb1-4a83-87af-061a0cfaa24a
\.


--
-- Data for Name: brand_inbound_shipments; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_inbound_shipments (brand_id, inbound_shipment_id) FROM stdin;
\.


--
-- Data for Name: brand_initiatives; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_initiatives (brand_id, initiative_id) FROM stdin;
\.


--
-- Data for Name: brand_inventory_locations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_inventory_locations (brand_id, inventory_location_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	fe580eef-3696-4495-9be2-ab9becfeeafe
\.


--
-- Data for Name: brand_items; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_items (brand_id, item_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	7425a920-d427-4d2a-8b39-7b3fea22f6ba
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	e14e0921-71c0-4275-908f-c6b1157e397b
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	fb6fb5a9-e3d3-4075-8e61-0f3536048964
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	9e83ff72-096f-408f-956d-23fac489bfbe
\.


--
-- Data for Name: brand_observations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_observations (brand_id, observation_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	d52df011-eebd-48ff-9737-a29c458b9fbd
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	b03d03be-187e-4ba7-b8be-6f50e62f610e
\.


--
-- Data for Name: brand_partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_partners (brand_id, partner_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	76649aec-be4d-470d-8a99-3755da53c086
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	ad92f467-de6a-4c81-a50f-89d26d9537ea
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	6c43ab71-8ce6-4b81-aa6b-8120ff880b80
\.


--
-- Data for Name: brand_purchase_orders; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_purchase_orders (brand_id, purchase_order_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	65a34664-03b3-4f29-bd01-9f9f40b2cc86
\.


--
-- Data for Name: brand_sourcing_trips; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brand_sourcing_trips (brand_id, sourcing_trip_id) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	4e01d9c9-8e1d-4c28-a076-0abb61c27d57
\.


--
-- Data for Name: brands; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.brands (id, name, slug, description, status, created_at, updated_at) FROM stdin;
83c2b556-2e7f-4d5c-885a-77c22dffe3cc	SUMA	suma	Hair and care brand rooted in the principles of sustainability, wellness, and culturally significant beautification. It is a brand that celebrates the beauty of Black hair and skin, bringing centuries old traditions into modern formulations and applications. SUMA is committed to helping create a world that feels confident, imaginative, and grounded. The brand prioritizes safe, effective ingredients, as well as ethical production practices, thoughtful construction, and reliable hair solutions. This brand is very eager to make breakthroughs and contributions in the automation and beauty tech space, and is always looking for ways to improve the haircare experience. As a flagship brand within SHÉ Estate, SUMA combines product innovation with an emphasis on quality, longevity, and intentional production.	active	2026-10-21 00:17:47.020433+00	2026-10-21 00:17:47.020433+00
ab9a4615-ee5b-4e31-ae9f-500faa202a26	TUFA	tufa	Fashion brand rooted in cultural expression, intentional design, enduring craftsmanship, and sustainability. It approaches fashion as a way to communicate sense of self, creating pieces that deserve to be worn, kept, and passsed down. TUFA is helping create a world that feels connected, introspective, and forward-looking. The brand prioritizes natural, durable fabrics, and ethical production practices, while also exploring new technologies and materials. TUFA is about fashion as identity, expression, and possibility: honoring where we came from while imagining where we can go. As with many brands within the Estate, TUFA favors made-to-order, small batch, and limited-run production over mass production.	active	2026-10-21 00:17:47.258745+00	2026-10-21 00:17:47.258745+00
2a676c77-761e-4dd6-826c-7c9d25fd47ce	GIDA	gida	Home and lifestyle brand rooted in intentional living, considered design, enduring craftsmanship, and sustainability. It approaches the home as an expression of belonging, taste, and comforts. GIDA is helping create a world that harmonious, timeless, and efficient. The brand prioritizes durability and indegenous materials and production, while exploring method improvements and sustainable practices. GIDA is about the home as a place of recalibration, being recharged by the things that help us function at our best and see the beauty in the world around us. As with many brands within the Estate, GIDA favors made-to-order, small batch, and limited-run production over mass production. Enduring over disposable.	active	2026-10-21 00:17:47.28919+00	2026-10-21 00:17:47.28919+00
a6cac39b-fdba-4fb0-b0cb-05af1d151861	AMSA	amsa	Technology and creative studio: software, SEO, AI automation, design, social. An answer. A response. A way forward. AMSA provides consulting, contract engineering, software development, systems integration, automation, technical implementation, and new product development. It is a flexible technical partner that can advise, design, troubleshoot, build, integrate, and deliver through contracted expertise. To whatever comes next.	active	2026-10-21 00:17:47.318743+00	2026-10-21 00:17:47.318743+00
\.


--
-- Data for Name: decision_inbound_shipments; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decision_inbound_shipments (decision_id, inbound_shipment_id) FROM stdin;
\.


--
-- Data for Name: decision_inventory_locations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decision_inventory_locations (decision_id, inventory_location_id) FROM stdin;
\.


--
-- Data for Name: decision_inventory_movements; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decision_inventory_movements (decision_id, inventory_movement_id) FROM stdin;
\.


--
-- Data for Name: decision_items; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decision_items (decision_id, item_id) FROM stdin;
14a51e18-4fb1-4a83-87af-061a0cfaa24a	fb6fb5a9-e3d3-4075-8e61-0f3536048964
\.


--
-- Data for Name: decision_partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decision_partners (decision_id, partner_id) FROM stdin;
\.


--
-- Data for Name: decision_purchase_orders; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decision_purchase_orders (decision_id, purchase_order_id) FROM stdin;
\.


--
-- Data for Name: decisions; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.decisions (id, title, decision_summary, reasoning, status, decided_at, created_at, updated_at) FROM stdin;
14a51e18-4fb1-4a83-87af-061a0cfaa24a	Limit production runs to 500 units	Cap each SUMA production run at 500 units.	Preserves small-batch quality and scarcity while managing cost risk.	in_effect	2026-03-20 00:00:00+00	2026-10-21 02:43:09.032628+00	2026-10-21 02:43:09.032628+00
\.


--
-- Data for Name: field_notes; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.field_notes (id, slug, title, status, theme, poem, media, essay, excerpt, initiative_id, published_at, created_at, updated_at, sources, tags) FROM stdin;
e06279e0-8b4f-4448-bd77-d9cd6b7fe4b0	counsel	COUNSEL IS NOT THE DECISION	published	ai synthesis	\n\nThe woman walks alone in the fields,\nQuerying the horizon for signs of life,\nOutward is her reach.\n\nThe machine responds,\nVast in the expanse of its knowledge, and status.\n\nIt answered in full, then wrote nothing down.\n\nCertainty was a field on the draft, and the draft is not the record.\n\nSnapped back to the walls of her own consciousness,\nShe ponders the weight of knowledge.\n\nBraced with the courage of convention,\nShe forges ahead.\n\nRead. Weigh. Commit.\n\n	[{"alt": "placeholder", "url": "https://placehold.co/1200x1600/111334/e9e7f6?text=01", "kind": "image", "caption": "draft"}, {"alt": "placeholder", "url": "https://placehold.co/1600x1200/12142e/e9e7f6?text=02", "kind": "image", "caption": "commit"}]	\n\nThe synthesize endpoint reads an initiative's observations and drafts a decision from it/them with Claude. It returns that draft and writes nothing. A human reads it and commits through the normal decision flow, or not.\n\nThe machine never has the last move. \n\nThree choices shaped it:\n- output is pulled through forced tool-use so the model returns a structured draft instead of prose.\n- confidence is a draft-only field; it is set by the model and dropped at commit.\n- drafts always have the source_observation_ids, so there's evidence where the draft originated.\n\nFirst light was on the far side of four errors:\n- 500: an empty key\n- 401: a key-name mismaatch\n- 502: a strict confidence enum \n- a quiet repo-pattern bug\n\nIn the end, the feature was shipped in less than a day.\n\nTo summarize, \n- we owe it to ourselves to take the time to parse data, to weigh options, and to forge ahead. \n- the race towards betterment includes the slow and deliberate steps.\n- * one more things about human first or responsible ai use.\n\nThanks for stopping by!\n\n	Read. Weigh. Commit.	\N	2026-10-20 19:51:57.924577+00	2026-10-20 19:51:57.602314+00	2026-10-20 19:51:57.923645+00	[{"url": null, "kind": "repo", "label": "synthesize endpoint ()"}, {"url": "https://platform.claude.com/docs/en/models/sonnet-5/overview", "kind": "doc", "label": "Claude Sonnet"}, {"url": "https://www.anthropic.com/research/team/interpretability", "kind": "doc", "label": "responsible AI | human-in-the-loop"}]	null
\.


--
-- Data for Name: inbound_shipment_lines; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inbound_shipment_lines (id, inbound_shipment_id, purchase_order_line_id, quantity_shipped, quantity_received, quantity_accepted, quantity_damaged, unit_of_measure_id, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: inbound_shipments; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inbound_shipments (id, inbound_shipment_number, status, tracking_number, carrier_name, destination_inventory_location_id, shipped_at, received_at, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: initiative_decisions; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_decisions (initiative_id, decision_id) FROM stdin;
\.


--
-- Data for Name: initiative_inbound_shipments; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_inbound_shipments (initiative_id, inbound_shipment_id) FROM stdin;
\.


--
-- Data for Name: initiative_inventory_locations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_inventory_locations (initiative_id, inventory_location_id) FROM stdin;
\.


--
-- Data for Name: initiative_items; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_items (initiative_id, item_id) FROM stdin;
\.


--
-- Data for Name: initiative_observations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_observations (initiative_id, observation_id) FROM stdin;
\.


--
-- Data for Name: initiative_partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_partners (initiative_id, partner_id) FROM stdin;
\.


--
-- Data for Name: initiative_purchase_orders; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_purchase_orders (initiative_id, purchase_order_id) FROM stdin;
\.


--
-- Data for Name: initiative_sourcing_trips; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_sourcing_trips (initiative_id, sourcing_trip_id) FROM stdin;
\.


--
-- Data for Name: initiative_types; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiative_types (id, name, slug, description, is_active, created_at, updated_at) FROM stdin;
33333333-0000-4000-8000-000000000001	collection	collection	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
33333333-0000-4000-8000-000000000002	research	research	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
33333333-0000-4000-8000-000000000003	social_impact_program	social_impact_program	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
33333333-0000-4000-8000-000000000004	publishing	publishing	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
\.


--
-- Data for Name: initiatives; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.initiatives (id, initiative_type_id, name, slug, description, status, start_date, end_date, created_at, updated_at) FROM stdin;
c8b5332b-438f-4735-89bf-0582faf8220d	33333333-0000-4000-8000-000000000004	Editions	editions	The library of media. Houses field notes and published media, of varied formats, across the estate.	active	\N	\N	2026-10-21 00:17:47.352308+00	2026-10-21 00:17:47.352308+00
5cff35d7-303a-40ef-8413-75a64e2699a6	33333333-0000-4000-8000-000000000003	SHÉRocks	she_rocks	Social impact program to support Black girls/women in STEAM. It aims to act as a gateway to scientific discovery, cultural appreciation, creative exploration, and technical skill-building. The initiative supports girls through fundraising, educational resources, mentorship, and community-building. As an initiative, SHÉRocks leverages the Estate's resouces, relationships, and ecosystem to turn awareness into action, and create lasting community value.	active	\N	\N	2026-10-21 00:17:47.436979+00	2026-10-21 00:17:47.436979+00
\.


--
-- Data for Name: inventory_balances; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inventory_balances (id, item_id, inventory_location_id, quantity_on_hand, unit_of_measure_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: inventory_location_types; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inventory_location_types (id, name, slug, description, is_active, created_at, updated_at) FROM stdin;
44444444-0000-4000-8000-000000000001	warehouse	warehouse	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
44444444-0000-4000-8000-000000000002	studio	studio	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
44444444-0000-4000-8000-000000000003	production_site	production_site	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
44444444-0000-4000-8000-000000000004	event	event	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
44444444-0000-4000-8000-000000000005	temporary_storage	temporary_storage	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
\.


--
-- Data for Name: inventory_locations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inventory_locations (id, inventory_location_type_id, name, slug, description, status, address_line_1, address_line_2, city, region, postal_code, country_code, active_from, active_until, created_at, updated_at) FROM stdin;
fe580eef-3696-4495-9be2-ab9becfeeafe	44444444-0000-4000-8000-000000000001	Abuja Warehouse	abuja_warehouse	Primary SUMA storage.	active	Lugbe	\N	Abuja	FCT	\N	NG	\N	\N	2026-10-21 02:43:08.621792+00	2026-10-21 02:43:08.621792+00
\.


--
-- Data for Name: inventory_movement_types; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inventory_movement_types (id, name, slug, description, is_active, created_at, updated_at) FROM stdin;
55555555-0000-4000-8000-000000000001	receipt	receipt	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000002	transfer_in	transfer_in	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000003	transfer_out	transfer_out	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000004	adjustment_in	adjustment_in	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000005	adjustment_out	adjustment_out	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000006	damage	damage	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000007	loss	loss	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000008	consumption	consumption	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000009	sample	sample	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
55555555-0000-4000-8000-000000000010	return_to_stock	return_to_stock	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
\.


--
-- Data for Name: inventory_movements; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.inventory_movements (id, item_id, inventory_location_id, inventory_movement_type_id, inbound_shipment_line_id, related_movement_id, quantity_delta, unit_of_measure_id, occurred_at, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: item_partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.item_partners (item_id, partner_id) FROM stdin;
7425a920-d427-4d2a-8b39-7b3fea22f6ba	76649aec-be4d-470d-8a99-3755da53c086
\.


--
-- Data for Name: item_types; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.item_types (id, name, slug, description, is_active, created_at, updated_at) FROM stdin;
11111111-0000-4000-8000-000000000001	material	material	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
11111111-0000-4000-8000-000000000002	component	component	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
11111111-0000-4000-8000-000000000003	sample	sample	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
11111111-0000-4000-8000-000000000004	finished_product	finished_product	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
11111111-0000-4000-8000-000000000005	packaging	packaging	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
11111111-0000-4000-8000-000000000006	asset	asset	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.items (id, name, slug, sku, item_type_id, description, status, created_at, updated_at) FROM stdin;
7425a920-d427-4d2a-8b39-7b3fea22f6ba	Human Hair Bundle 10in	human_hair_bundle_10in	SUMA-HHB-10	11111111-0000-4000-8000-000000000001	Raw human hair bundle, 10 inch.	active	2026-10-21 02:43:08.344404+00	2026-10-21 02:43:08.344404+00
e14e0921-71c0-4275-908f-c6b1157e397b	Full Lace Cap	full_lace_cap	SUMA-FLC	11111111-0000-4000-8000-000000000002	Full lace wig cap.	active	2026-10-21 02:43:08.465401+00	2026-10-21 02:43:08.465401+00
fb6fb5a9-e3d3-4075-8e61-0f3536048964	Mutinta Licorice 10in	mutinta_10in_licorice	SUMA-MUT-10-LIC	11111111-0000-4000-8000-000000000004	Finished Mutinta wig, licorice, 10 inch.	active	2026-10-21 02:43:08.494607+00	2026-10-21 02:43:08.494607+00
9e83ff72-096f-408f-956d-23fac489bfbe	SUMA Packaging Box	suma_packaging_box	SUMA-PKG-BOX	11111111-0000-4000-8000-000000000005	Branded packaging box.	inactive	2026-10-21 02:43:08.509286+00	2026-10-21 02:43:08.509286+00
7d453d60-b87e-40af-b317-59899fff5095	Miriam Licorice 14in	miriam_14in_licorice	SUMA-MIR-14-LIC	11111111-0000-4000-8000-000000000004	Finished Miriam wig, licorice, 14 inch.	active	2026-10-21 14:20:05.131242+00	2026-10-21 14:20:05.131242+00
cfb28cf8-f9a0-421e-8f3f-b5311d86c61f	Hatshepsut Licorice 14in	hatshepsut_14in_licorice	SUMA-HAT-14-LIC	11111111-0000-4000-8000-000000000004	Finished Hatshepsut wig, licorice, 14 inch.	active	2026-10-21 14:22:55.901283+00	2026-10-21 14:22:55.901283+00
69b34266-52fd-4838-a889-7a24ad335572	Amina Licorice 14in	amina_14in_licorice	SUMA-AMINA-14-LIC	11111111-0000-4000-8000-000000000004	Finished Amina wig, licorice, 14 inch.	active	2026-10-21 14:25:30.485814+00	2026-10-21 14:25:30.485814+00
44022e6f-c95d-41b6-9858-7c991da3cbec	Amina Licorice 8in	amina_8in_licorice	SUMA-AMINA-8-LIC	11111111-0000-4000-8000-000000000004	Finished Amina wig, licorice, 8 inch.	active	2026-10-21 14:27:19.056937+00	2026-10-21 14:27:19.056937+00
002f0a21-3e11-4c4d-9205-cd72aaa04a28	Hileni Licorice 14in	hileni_14in_licorice	SUMA-HILENI-14-LIC	11111111-0000-4000-8000-000000000004	Finished Hileni wig, licorice, 14 inch.	active	2026-10-21 14:32:32.273158+00	2026-10-21 14:32:32.273158+00
80fb52a1-957a-4291-903a-ae32ea77d50f	Kemi Licorice 8in	kemi_8in_licorice	SUMA-KEMI-8-LIC	11111111-0000-4000-8000-000000000004	Finished Kemi wig, licorice, 8 inch.	active	2026-10-21 14:34:39.309009+00	2026-10-21 14:34:39.309009+00
60f6ffd2-d521-4eae-8a3c-c30be4684787	Rusika Licorice 12in	rusika_12in_licorice	SUMA-RUSIKA-12-LIC	11111111-0000-4000-8000-000000000004	Finished Rusika wig, licorice, 12 inch.	active	2026-10-21 19:03:06.570203+00	2026-10-21 19:03:06.570203+00
346857c4-9dde-47f3-9437-2b9c5adb904a	Ina Licorice 14in	ina_14in_licorice	SUMA-INA-14-LIC	11111111-0000-4000-8000-000000000004	Finished Ina wig, licorice, 14 inch.	active	2026-10-21 19:05:18.987429+00	2026-10-21 19:05:18.987429+00
0e48cc05-8d07-456b-b3de-6c89f7707dcd	Linda Licorice 8in	linda_8in_licorice	SUMA-LINDA-8-LIC	11111111-0000-4000-8000-000000000004	Finished Linda wig, licorice, 8 inch.	active	2026-10-21 19:07:40.167511+00	2026-10-21 19:07:40.167511+00
f92577dd-def5-444a-b31d-7ffaa14853ee	Binta Licorice 10in	binta_10in_licorice	SUMA-BINTA-10-LIC	11111111-0000-4000-8000-000000000004	Finished Binta wig, licorice, 10 inch.	active	2026-10-21 19:09:57.49843+00	2026-10-21 19:09:57.49843+00
72dbc1e4-369e-4afe-bb22-c74546beaf0b	Hanta Licorice 10in	hanta_10in_licorice	SUMA-HANTA-10-LIC	11111111-0000-4000-8000-000000000004	Finished Hanta wig, licorice, 10 inch.	active	2026-10-21 19:13:19.998346+00	2026-10-21 19:13:19.998346+00
d523457b-377f-4bc0-87fa-e9807a09ba6a	Nina Licorice 4in	nina_4in_licorice	SUMA-NINA-4-LIC	11111111-0000-4000-8000-000000000004	Finished Nina wig, licorice, 4 inch.	active	2026-10-21 14:31:15.426659+00	2026-10-21 19:39:10.048137+00
\.


--
-- Data for Name: observation_decisions; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_decisions (observation_id, decision_id) FROM stdin;
\.


--
-- Data for Name: observation_inbound_shipments; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_inbound_shipments (observation_id, inbound_shipment_id) FROM stdin;
\.


--
-- Data for Name: observation_inventory_locations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_inventory_locations (observation_id, inventory_location_id) FROM stdin;
\.


--
-- Data for Name: observation_inventory_movements; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_inventory_movements (observation_id, inventory_movement_id) FROM stdin;
\.


--
-- Data for Name: observation_items; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_items (observation_id, item_id) FROM stdin;
\.


--
-- Data for Name: observation_partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_partners (observation_id, partner_id) FROM stdin;
\.


--
-- Data for Name: observation_purchase_orders; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observation_purchase_orders (observation_id, purchase_order_id) FROM stdin;
\.


--
-- Data for Name: observations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.observations (id, title, details, observed_at, created_at, updated_at) FROM stdin;
d52df011-eebd-48ff-9737-a29c458b9fbd	Automation interest in braiding tools	Growing industry interest in automation tools for braiding; a clear opening for SUMA in the beauty-tech space. We should explore partnerships with braiding tool manufacturers and with robotics labs to develop a prototype braiding machine. A good place to start would be to reach out to the AI team from MUShanghai that presented their nail virtual try on tool at the 2026 spring conference.	2026-10-20 09:30:00+00	2026-10-21 02:43:08.779331+00	2026-10-21 02:43:08.779331+00
b03d03be-187e-4ba7-b8be-6f50e62f610e	Plant-based braiding hair demand	Rising demand for plant-based, biodegradable braiding hair among conscious consumers.	2026-03-15 11:00:00+00	2026-10-21 02:43:08.81363+00	2026-10-21 02:43:08.81363+00
\.


--
-- Data for Name: partner_types; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.partner_types (id, name, slug, description, is_active, created_at, updated_at) FROM stdin;
22222222-0000-4000-8000-000000000001	supplier	supplier	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
22222222-0000-4000-8000-000000000002	manufacturer	manufacturer	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
22222222-0000-4000-8000-000000000003	crafter	crafter	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
22222222-0000-4000-8000-000000000004	tailor	tailor	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
22222222-0000-4000-8000-000000000005	pattern_maker	pattern_maker	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
22222222-0000-4000-8000-000000000006	technical_designer	technical_designer	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
22222222-0000-4000-8000-000000000007	logistics_provider	logistics_provider	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
\.


--
-- Data for Name: partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.partners (id, name, slug, partner_type_id, description, status, website, email, phone, created_at, updated_at) FROM stdin;
76649aec-be4d-470d-8a99-3755da53c086	Nancy Nwachukwu	nancy_nwachukwu	22222222-0000-4000-8000-000000000003	Hair shop owner, braider, and assistant in Abuja. Resides in Mpape, Nigeria. Manages a team of over 7 braiders, finishers, and ventilators.	active	\N	\N	\N	2026-10-21 02:43:07.928041+00	2026-10-21 02:43:07.928041+00
ad92f467-de6a-4c81-a50f-89d26d9537ea	Outre X-Pression	outre_xpression	22222222-0000-4000-8000-000000000002	Synthetic and protective-style hair manufacturer.	inactive	\N	\N	\N	2026-10-21 02:43:08.11236+00	2026-10-21 02:43:08.11236+00
6c43ab71-8ce6-4b81-aa6b-8120ff880b80	DHL Nigeria	dhl_nigeria	22222222-0000-4000-8000-000000000007	International logistics provider.	inactive	\N	\N	\N	2026-10-21 02:43:08.137527+00	2026-10-21 02:43:08.137527+00
\.


--
-- Data for Name: purchase_order_lines; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.purchase_order_lines (id, purchase_order_id, item_id, line_number, description, quantity_ordered, unit_of_measure_id, unit_price, created_at, updated_at) FROM stdin;
0464f8dd-cf63-405e-ab21-ce59ec90479f	65a34664-03b3-4f29-bd01-9f9f40b2cc86	69b34266-52fd-4838-a889-7a24ad335572	1	Finished Amina wig, licorice, 14 inch.	10.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:18:50.931404+00	2026-10-21 19:18:50.931404+00
2f2ca9fb-8d57-4cc6-ae24-f107509b8683	65a34664-03b3-4f29-bd01-9f9f40b2cc86	44022e6f-c95d-41b6-9858-7c991da3cbec	2	Finished Amina wig, licorice, 8 inch.	10.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:19:39.219433+00	2026-10-21 19:19:39.219433+00
80c10e61-3c1c-467d-a610-7c7cd5c7f0b0	65a34664-03b3-4f29-bd01-9f9f40b2cc86	f92577dd-def5-444a-b31d-7ffaa14853ee	3	Finished Binta wig, licorice, 10 inch.	10.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:20:37.758581+00	2026-10-21 19:20:37.758581+00
d0b7b9c6-73d2-4982-b79f-25474130c933	65a34664-03b3-4f29-bd01-9f9f40b2cc86	72dbc1e4-369e-4afe-bb22-c74546beaf0b	4	Finished Hanta wig, licorice, 10 inch.	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:21:48.627368+00	2026-10-21 19:21:48.627368+00
85383fec-7a18-44d2-8c5e-3853764e10d2	65a34664-03b3-4f29-bd01-9f9f40b2cc86	72dbc1e4-369e-4afe-bb22-c74546beaf0b	5	Finished Hatshepsut wig, licorice, 14 inch.	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:22:15.217117+00	2026-10-21 19:22:15.217117+00
63746ea1-d4be-429f-9750-0cb29a47bcd0	65a34664-03b3-4f29-bd01-9f9f40b2cc86	002f0a21-3e11-4c4d-9205-cd72aaa04a28	6	Finished Hileni wig, licorice, 14 inch.	10.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:22:51.204525+00	2026-10-21 19:22:51.204525+00
cf347e32-4814-48eb-8614-b01c898cb49d	65a34664-03b3-4f29-bd01-9f9f40b2cc86	346857c4-9dde-47f3-9437-2b9c5adb904a	7	Finished Ina wig, licorice, 14 inch.	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:23:35.824474+00	2026-10-21 19:23:35.824474+00
a81ec9ed-dfcb-434d-8427-07b97628666f	65a34664-03b3-4f29-bd01-9f9f40b2cc86	80fb52a1-957a-4291-903a-ae32ea77d50f	8	Finished Kemi wig, licorice, 8 inch.	10.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:24:26.82192+00	2026-10-21 19:24:26.82192+00
9db80197-30c4-4194-89a5-20343a378ad5	65a34664-03b3-4f29-bd01-9f9f40b2cc86	0e48cc05-8d07-456b-b3de-6c89f7707dcd	9	Finished Linda wig, licorice, 8 inch.	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:25:05.123216+00	2026-10-21 19:25:05.123216+00
03166a58-fbff-49a1-8c2c-73cc024aa4b9	65a34664-03b3-4f29-bd01-9f9f40b2cc86	7d453d60-b87e-40af-b317-59899fff5095	10	Finished Miriam wig, licorice, 14 inch.	10.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:27:39.706996+00	2026-10-21 19:27:39.706996+00
e4ba8e72-6dd1-4cf8-bc5a-87fcc2f75764	65a34664-03b3-4f29-bd01-9f9f40b2cc86	fb6fb5a9-e3d3-4075-8e61-0f3536048964	11	Finished Mutinta wig, licorice, 10 inch..	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:31:30.050631+00	2026-10-21 19:31:30.050631+00
f4b69e07-df40-45a0-8acb-3e61756d7b1e	65a34664-03b3-4f29-bd01-9f9f40b2cc86	d523457b-377f-4bc0-87fa-e9807a09ba6a	12	Finished Nina wig, licorice, 4 inch.	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:32:26.9229+00	2026-10-21 19:32:26.9229+00
b3cb7f03-fc08-4aee-9782-66b9de05c3f7	65a34664-03b3-4f29-bd01-9f9f40b2cc86	60f6ffd2-d521-4eae-8a3c-c30be4684787	13	Finished Rusika wig, licorice, 12 inch.	20.0000	66666666-0000-4000-8000-000000000001	\N	2026-10-21 19:33:05.56291+00	2026-10-21 19:33:05.56291+00
\.


--
-- Data for Name: purchase_orders; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.purchase_orders (id, purchase_order_number, partner_id, status, order_date, expected_date, currency_code, notes, created_at, updated_at, production_brief) FROM stdin;
65a34664-03b3-4f29-bd01-9f9f40b2cc86	SHE-PO-1003	76649aec-be4d-470d-8a99-3755da53c086	draft	2026-12-01	2027-01-30	NGN	I will make the exact selections.	2026-10-21 14:09:20.045265+00	2026-10-21 14:09:20.045265+00	Wigs for older women. Focus on shorter styles and colors older women gravitate toward.
\.


--
-- Data for Name: sourcing_trip_decisions; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trip_decisions (sourcing_trip_id, decision_id) FROM stdin;
\.


--
-- Data for Name: sourcing_trip_inbound_shipments; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trip_inbound_shipments (sourcing_trip_id, inbound_shipment_id) FROM stdin;
\.


--
-- Data for Name: sourcing_trip_items; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trip_items (sourcing_trip_id, item_id) FROM stdin;
4e01d9c9-8e1d-4c28-a076-0abb61c27d57	7425a920-d427-4d2a-8b39-7b3fea22f6ba
\.


--
-- Data for Name: sourcing_trip_observations; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trip_observations (sourcing_trip_id, observation_id) FROM stdin;
4e01d9c9-8e1d-4c28-a076-0abb61c27d57	b03d03be-187e-4ba7-b8be-6f50e62f610e
\.


--
-- Data for Name: sourcing_trip_partners; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trip_partners (sourcing_trip_id, partner_id) FROM stdin;
4e01d9c9-8e1d-4c28-a076-0abb61c27d57	76649aec-be4d-470d-8a99-3755da53c086
\.


--
-- Data for Name: sourcing_trip_purchase_orders; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trip_purchase_orders (sourcing_trip_id, purchase_order_id) FROM stdin;
\.


--
-- Data for Name: sourcing_trips; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.sourcing_trips (id, name, slug, description, status, start_date, end_date, created_at, updated_at) FROM stdin;
4e01d9c9-8e1d-4c28-a076-0abb61c27d57	Oriental Spring 26	oriental_spring_26	China and Vietnam sourcing trip.	completed	2026-05-08	2026-06-08	2026-10-21 02:43:08.668713+00	2026-10-21 02:43:08.668713+00
\.


--
-- Data for Name: units_of_measure; Type: TABLE DATA; Schema: public; Owner: she_os_user
--

COPY public.units_of_measure (id, name, slug, description, is_active, created_at, updated_at) FROM stdin;
66666666-0000-4000-8000-000000000001	piece	piece	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000002	bundle	bundle	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000003	set	set	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000004	pair	pair	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000005	yard	yard	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000006	meter	meter	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000007	centimeter	centimeter	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000008	kilogram	kilogram	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000009	gram	gram	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000010	liter	liter	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000011	milliliter	milliliter	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000012	roll	roll	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000013	spool	spool	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000014	box	box	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
66666666-0000-4000-8000-000000000015	carton	carton	\N	t	2026-10-19 01:39:58.585035+00	2026-10-19 01:39:58.585035+00
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: inventory_balances item_location_unique; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_balances
    ADD CONSTRAINT item_location_unique UNIQUE (item_id, inventory_location_id);


--
-- Name: brand_decisions pk_brand_decisions; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_decisions
    ADD CONSTRAINT pk_brand_decisions PRIMARY KEY (brand_id, decision_id);


--
-- Name: brand_inbound_shipments pk_brand_inbound_shipments; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_inbound_shipments
    ADD CONSTRAINT pk_brand_inbound_shipments PRIMARY KEY (brand_id, inbound_shipment_id);


--
-- Name: brand_initiatives pk_brand_initiatives; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_initiatives
    ADD CONSTRAINT pk_brand_initiatives PRIMARY KEY (brand_id, initiative_id);


--
-- Name: brand_inventory_locations pk_brand_inventory_locations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_inventory_locations
    ADD CONSTRAINT pk_brand_inventory_locations PRIMARY KEY (brand_id, inventory_location_id);


--
-- Name: brand_items pk_brand_items; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_items
    ADD CONSTRAINT pk_brand_items PRIMARY KEY (brand_id, item_id);


--
-- Name: brand_observations pk_brand_observations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_observations
    ADD CONSTRAINT pk_brand_observations PRIMARY KEY (brand_id, observation_id);


--
-- Name: brand_partners pk_brand_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_partners
    ADD CONSTRAINT pk_brand_partners PRIMARY KEY (brand_id, partner_id);


--
-- Name: brand_purchase_orders pk_brand_purchase_orders; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_purchase_orders
    ADD CONSTRAINT pk_brand_purchase_orders PRIMARY KEY (brand_id, purchase_order_id);


--
-- Name: brand_sourcing_trips pk_brand_sourcing_trips; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_sourcing_trips
    ADD CONSTRAINT pk_brand_sourcing_trips PRIMARY KEY (brand_id, sourcing_trip_id);


--
-- Name: brands pk_brands; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT pk_brands PRIMARY KEY (id);


--
-- Name: decision_inbound_shipments pk_decision_inbound_shipments; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inbound_shipments
    ADD CONSTRAINT pk_decision_inbound_shipments PRIMARY KEY (decision_id, inbound_shipment_id);


--
-- Name: decision_inventory_locations pk_decision_inventory_locations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inventory_locations
    ADD CONSTRAINT pk_decision_inventory_locations PRIMARY KEY (decision_id, inventory_location_id);


--
-- Name: decision_inventory_movements pk_decision_inventory_movements; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inventory_movements
    ADD CONSTRAINT pk_decision_inventory_movements PRIMARY KEY (decision_id, inventory_movement_id);


--
-- Name: decision_items pk_decision_items; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_items
    ADD CONSTRAINT pk_decision_items PRIMARY KEY (decision_id, item_id);


--
-- Name: decision_partners pk_decision_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_partners
    ADD CONSTRAINT pk_decision_partners PRIMARY KEY (decision_id, partner_id);


--
-- Name: decision_purchase_orders pk_decision_purchase_orders; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_purchase_orders
    ADD CONSTRAINT pk_decision_purchase_orders PRIMARY KEY (decision_id, purchase_order_id);


--
-- Name: decisions pk_decisions; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decisions
    ADD CONSTRAINT pk_decisions PRIMARY KEY (id);


--
-- Name: field_notes pk_field_notes; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.field_notes
    ADD CONSTRAINT pk_field_notes PRIMARY KEY (id);


--
-- Name: inbound_shipment_lines pk_inbound_shipment_lines; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipment_lines
    ADD CONSTRAINT pk_inbound_shipment_lines PRIMARY KEY (id);


--
-- Name: inbound_shipments pk_inbound_shipments; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipments
    ADD CONSTRAINT pk_inbound_shipments PRIMARY KEY (id);


--
-- Name: initiative_decisions pk_initiative_decisions; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_decisions
    ADD CONSTRAINT pk_initiative_decisions PRIMARY KEY (initiative_id, decision_id);


--
-- Name: initiative_inbound_shipments pk_initiative_inbound_shipments; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_inbound_shipments
    ADD CONSTRAINT pk_initiative_inbound_shipments PRIMARY KEY (initiative_id, inbound_shipment_id);


--
-- Name: initiative_inventory_locations pk_initiative_inventory_locations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_inventory_locations
    ADD CONSTRAINT pk_initiative_inventory_locations PRIMARY KEY (initiative_id, inventory_location_id);


--
-- Name: initiative_items pk_initiative_items; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_items
    ADD CONSTRAINT pk_initiative_items PRIMARY KEY (initiative_id, item_id);


--
-- Name: initiative_observations pk_initiative_observations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_observations
    ADD CONSTRAINT pk_initiative_observations PRIMARY KEY (initiative_id, observation_id);


--
-- Name: initiative_partners pk_initiative_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_partners
    ADD CONSTRAINT pk_initiative_partners PRIMARY KEY (initiative_id, partner_id);


--
-- Name: initiative_purchase_orders pk_initiative_purchase_orders; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_purchase_orders
    ADD CONSTRAINT pk_initiative_purchase_orders PRIMARY KEY (initiative_id, purchase_order_id);


--
-- Name: initiative_sourcing_trips pk_initiative_sourcing_trips; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_sourcing_trips
    ADD CONSTRAINT pk_initiative_sourcing_trips PRIMARY KEY (initiative_id, sourcing_trip_id);


--
-- Name: initiative_types pk_initiative_types; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_types
    ADD CONSTRAINT pk_initiative_types PRIMARY KEY (id);


--
-- Name: initiatives pk_initiatives; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiatives
    ADD CONSTRAINT pk_initiatives PRIMARY KEY (id);


--
-- Name: inventory_balances pk_inventory_balances; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_balances
    ADD CONSTRAINT pk_inventory_balances PRIMARY KEY (id);


--
-- Name: inventory_location_types pk_inventory_location_types; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_location_types
    ADD CONSTRAINT pk_inventory_location_types PRIMARY KEY (id);


--
-- Name: inventory_locations pk_inventory_locations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_locations
    ADD CONSTRAINT pk_inventory_locations PRIMARY KEY (id);


--
-- Name: inventory_movement_types pk_inventory_movement_types; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movement_types
    ADD CONSTRAINT pk_inventory_movement_types PRIMARY KEY (id);


--
-- Name: inventory_movements pk_inventory_movements; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT pk_inventory_movements PRIMARY KEY (id);


--
-- Name: item_partners pk_item_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.item_partners
    ADD CONSTRAINT pk_item_partners PRIMARY KEY (item_id, partner_id);


--
-- Name: item_types pk_item_types; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.item_types
    ADD CONSTRAINT pk_item_types PRIMARY KEY (id);


--
-- Name: items pk_items; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT pk_items PRIMARY KEY (id);


--
-- Name: observation_decisions pk_observation_decisions; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_decisions
    ADD CONSTRAINT pk_observation_decisions PRIMARY KEY (observation_id, decision_id);


--
-- Name: observation_inbound_shipments pk_observation_inbound_shipments; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inbound_shipments
    ADD CONSTRAINT pk_observation_inbound_shipments PRIMARY KEY (observation_id, inbound_shipment_id);


--
-- Name: observation_inventory_locations pk_observation_inventory_locations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inventory_locations
    ADD CONSTRAINT pk_observation_inventory_locations PRIMARY KEY (observation_id, inventory_location_id);


--
-- Name: observation_inventory_movements pk_observation_inventory_movements; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inventory_movements
    ADD CONSTRAINT pk_observation_inventory_movements PRIMARY KEY (observation_id, inventory_movement_id);


--
-- Name: observation_items pk_observation_items; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_items
    ADD CONSTRAINT pk_observation_items PRIMARY KEY (observation_id, item_id);


--
-- Name: observation_partners pk_observation_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_partners
    ADD CONSTRAINT pk_observation_partners PRIMARY KEY (observation_id, partner_id);


--
-- Name: observation_purchase_orders pk_observation_purchase_orders; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_purchase_orders
    ADD CONSTRAINT pk_observation_purchase_orders PRIMARY KEY (observation_id, purchase_order_id);


--
-- Name: observations pk_observations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observations
    ADD CONSTRAINT pk_observations PRIMARY KEY (id);


--
-- Name: partner_types pk_partner_types; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.partner_types
    ADD CONSTRAINT pk_partner_types PRIMARY KEY (id);


--
-- Name: partners pk_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT pk_partners PRIMARY KEY (id);


--
-- Name: purchase_order_lines pk_purchase_order_lines; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_order_lines
    ADD CONSTRAINT pk_purchase_order_lines PRIMARY KEY (id);


--
-- Name: purchase_orders pk_purchase_orders; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT pk_purchase_orders PRIMARY KEY (id);


--
-- Name: sourcing_trip_decisions pk_sourcing_trip_decisions; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_decisions
    ADD CONSTRAINT pk_sourcing_trip_decisions PRIMARY KEY (sourcing_trip_id, decision_id);


--
-- Name: sourcing_trip_inbound_shipments pk_sourcing_trip_inbound_shipments; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_inbound_shipments
    ADD CONSTRAINT pk_sourcing_trip_inbound_shipments PRIMARY KEY (sourcing_trip_id, inbound_shipment_id);


--
-- Name: sourcing_trip_items pk_sourcing_trip_items; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_items
    ADD CONSTRAINT pk_sourcing_trip_items PRIMARY KEY (sourcing_trip_id, item_id);


--
-- Name: sourcing_trip_observations pk_sourcing_trip_observations; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_observations
    ADD CONSTRAINT pk_sourcing_trip_observations PRIMARY KEY (sourcing_trip_id, observation_id);


--
-- Name: sourcing_trip_partners pk_sourcing_trip_partners; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_partners
    ADD CONSTRAINT pk_sourcing_trip_partners PRIMARY KEY (sourcing_trip_id, partner_id);


--
-- Name: sourcing_trip_purchase_orders pk_sourcing_trip_purchase_orders; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_purchase_orders
    ADD CONSTRAINT pk_sourcing_trip_purchase_orders PRIMARY KEY (sourcing_trip_id, purchase_order_id);


--
-- Name: sourcing_trips pk_sourcing_trips; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trips
    ADD CONSTRAINT pk_sourcing_trips PRIMARY KEY (id);


--
-- Name: units_of_measure pk_units_of_measure; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.units_of_measure
    ADD CONSTRAINT pk_units_of_measure PRIMARY KEY (id);


--
-- Name: purchase_order_lines po_line_number_unique; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_order_lines
    ADD CONSTRAINT po_line_number_unique UNIQUE (purchase_order_id, line_number);


--
-- Name: inbound_shipment_lines shipment_po_line_unique; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipment_lines
    ADD CONSTRAINT shipment_po_line_unique UNIQUE (inbound_shipment_id, purchase_order_line_id);


--
-- Name: brands uq_brands_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT uq_brands_name UNIQUE (name);


--
-- Name: brands uq_brands_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT uq_brands_slug UNIQUE (slug);


--
-- Name: inbound_shipments uq_inbound_shipments_inbound_shipment_number; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipments
    ADD CONSTRAINT uq_inbound_shipments_inbound_shipment_number UNIQUE (inbound_shipment_number);


--
-- Name: initiative_types uq_initiative_types_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_types
    ADD CONSTRAINT uq_initiative_types_name UNIQUE (name);


--
-- Name: initiative_types uq_initiative_types_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_types
    ADD CONSTRAINT uq_initiative_types_slug UNIQUE (slug);


--
-- Name: initiatives uq_initiatives_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiatives
    ADD CONSTRAINT uq_initiatives_slug UNIQUE (slug);


--
-- Name: inventory_location_types uq_inventory_location_types_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_location_types
    ADD CONSTRAINT uq_inventory_location_types_name UNIQUE (name);


--
-- Name: inventory_location_types uq_inventory_location_types_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_location_types
    ADD CONSTRAINT uq_inventory_location_types_slug UNIQUE (slug);


--
-- Name: inventory_locations uq_inventory_locations_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_locations
    ADD CONSTRAINT uq_inventory_locations_slug UNIQUE (slug);


--
-- Name: inventory_movement_types uq_inventory_movement_types_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movement_types
    ADD CONSTRAINT uq_inventory_movement_types_name UNIQUE (name);


--
-- Name: inventory_movement_types uq_inventory_movement_types_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movement_types
    ADD CONSTRAINT uq_inventory_movement_types_slug UNIQUE (slug);


--
-- Name: item_types uq_item_types_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.item_types
    ADD CONSTRAINT uq_item_types_name UNIQUE (name);


--
-- Name: item_types uq_item_types_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.item_types
    ADD CONSTRAINT uq_item_types_slug UNIQUE (slug);


--
-- Name: items uq_items_sku; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT uq_items_sku UNIQUE (sku);


--
-- Name: items uq_items_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT uq_items_slug UNIQUE (slug);


--
-- Name: partner_types uq_partner_types_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.partner_types
    ADD CONSTRAINT uq_partner_types_name UNIQUE (name);


--
-- Name: partner_types uq_partner_types_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.partner_types
    ADD CONSTRAINT uq_partner_types_slug UNIQUE (slug);


--
-- Name: partners uq_partners_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT uq_partners_slug UNIQUE (slug);


--
-- Name: purchase_orders uq_purchase_orders_purchase_order_number; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT uq_purchase_orders_purchase_order_number UNIQUE (purchase_order_number);


--
-- Name: sourcing_trips uq_sourcing_trips_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trips
    ADD CONSTRAINT uq_sourcing_trips_slug UNIQUE (slug);


--
-- Name: units_of_measure uq_units_of_measure_name; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.units_of_measure
    ADD CONSTRAINT uq_units_of_measure_name UNIQUE (name);


--
-- Name: units_of_measure uq_units_of_measure_slug; Type: CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.units_of_measure
    ADD CONSTRAINT uq_units_of_measure_slug UNIQUE (slug);


--
-- Name: ix_brand_decisions_decision_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_decisions_decision_id ON public.brand_decisions USING btree (decision_id);


--
-- Name: ix_brand_inbound_shipments_inbound_shipment_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_inbound_shipments_inbound_shipment_id ON public.brand_inbound_shipments USING btree (inbound_shipment_id);


--
-- Name: ix_brand_initiatives_initiative_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_initiatives_initiative_id ON public.brand_initiatives USING btree (initiative_id);


--
-- Name: ix_brand_inventory_locations_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_inventory_locations_inventory_location_id ON public.brand_inventory_locations USING btree (inventory_location_id);


--
-- Name: ix_brand_items_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_items_item_id ON public.brand_items USING btree (item_id);


--
-- Name: ix_brand_observations_observation_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_observations_observation_id ON public.brand_observations USING btree (observation_id);


--
-- Name: ix_brand_partners_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_partners_partner_id ON public.brand_partners USING btree (partner_id);


--
-- Name: ix_brand_purchase_orders_purchase_order_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_purchase_orders_purchase_order_id ON public.brand_purchase_orders USING btree (purchase_order_id);


--
-- Name: ix_brand_sourcing_trips_sourcing_trip_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_brand_sourcing_trips_sourcing_trip_id ON public.brand_sourcing_trips USING btree (sourcing_trip_id);


--
-- Name: ix_decision_inbound_shipments_inbound_shipment_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decision_inbound_shipments_inbound_shipment_id ON public.decision_inbound_shipments USING btree (inbound_shipment_id);


--
-- Name: ix_decision_inventory_locations_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decision_inventory_locations_inventory_location_id ON public.decision_inventory_locations USING btree (inventory_location_id);


--
-- Name: ix_decision_inventory_movements_inventory_movement_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decision_inventory_movements_inventory_movement_id ON public.decision_inventory_movements USING btree (inventory_movement_id);


--
-- Name: ix_decision_items_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decision_items_item_id ON public.decision_items USING btree (item_id);


--
-- Name: ix_decision_partners_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decision_partners_partner_id ON public.decision_partners USING btree (partner_id);


--
-- Name: ix_decision_purchase_orders_purchase_order_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decision_purchase_orders_purchase_order_id ON public.decision_purchase_orders USING btree (purchase_order_id);


--
-- Name: ix_decisions_decided_at; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decisions_decided_at ON public.decisions USING btree (decided_at);


--
-- Name: ix_decisions_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_decisions_status ON public.decisions USING btree (status);


--
-- Name: ix_field_notes_initiative_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_field_notes_initiative_id ON public.field_notes USING btree (initiative_id);


--
-- Name: ix_field_notes_published_at; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_field_notes_published_at ON public.field_notes USING btree (published_at);


--
-- Name: ix_field_notes_slug; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE UNIQUE INDEX ix_field_notes_slug ON public.field_notes USING btree (slug);


--
-- Name: ix_field_notes_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_field_notes_status ON public.field_notes USING btree (status);


--
-- Name: ix_inbound_shipment_lines_inbound_shipment_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inbound_shipment_lines_inbound_shipment_id ON public.inbound_shipment_lines USING btree (inbound_shipment_id);


--
-- Name: ix_inbound_shipment_lines_purchase_order_line_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inbound_shipment_lines_purchase_order_line_id ON public.inbound_shipment_lines USING btree (purchase_order_line_id);


--
-- Name: ix_inbound_shipments_destination_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inbound_shipments_destination_inventory_location_id ON public.inbound_shipments USING btree (destination_inventory_location_id);


--
-- Name: ix_inbound_shipments_received_at; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inbound_shipments_received_at ON public.inbound_shipments USING btree (received_at);


--
-- Name: ix_inbound_shipments_shipped_at; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inbound_shipments_shipped_at ON public.inbound_shipments USING btree (shipped_at);


--
-- Name: ix_inbound_shipments_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inbound_shipments_status ON public.inbound_shipments USING btree (status);


--
-- Name: ix_initiative_decisions_decision_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_decisions_decision_id ON public.initiative_decisions USING btree (decision_id);


--
-- Name: ix_initiative_inbound_shipments_inbound_shipment_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_inbound_shipments_inbound_shipment_id ON public.initiative_inbound_shipments USING btree (inbound_shipment_id);


--
-- Name: ix_initiative_inventory_locations_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_inventory_locations_inventory_location_id ON public.initiative_inventory_locations USING btree (inventory_location_id);


--
-- Name: ix_initiative_items_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_items_item_id ON public.initiative_items USING btree (item_id);


--
-- Name: ix_initiative_observations_observation_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_observations_observation_id ON public.initiative_observations USING btree (observation_id);


--
-- Name: ix_initiative_partners_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_partners_partner_id ON public.initiative_partners USING btree (partner_id);


--
-- Name: ix_initiative_purchase_orders_purchase_order_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_purchase_orders_purchase_order_id ON public.initiative_purchase_orders USING btree (purchase_order_id);


--
-- Name: ix_initiative_sourcing_trips_sourcing_trip_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_sourcing_trips_sourcing_trip_id ON public.initiative_sourcing_trips USING btree (sourcing_trip_id);


--
-- Name: ix_initiative_types_is_active; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiative_types_is_active ON public.initiative_types USING btree (is_active);


--
-- Name: ix_initiatives_initiative_type_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiatives_initiative_type_id ON public.initiatives USING btree (initiative_type_id);


--
-- Name: ix_initiatives_start_date; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiatives_start_date ON public.initiatives USING btree (start_date);


--
-- Name: ix_initiatives_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_initiatives_status ON public.initiatives USING btree (status);


--
-- Name: ix_inventory_balances_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_balances_inventory_location_id ON public.inventory_balances USING btree (inventory_location_id);


--
-- Name: ix_inventory_balances_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_balances_item_id ON public.inventory_balances USING btree (item_id);


--
-- Name: ix_inventory_location_types_is_active; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_location_types_is_active ON public.inventory_location_types USING btree (is_active);


--
-- Name: ix_inventory_locations_city; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_locations_city ON public.inventory_locations USING btree (city);


--
-- Name: ix_inventory_locations_country_code; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_locations_country_code ON public.inventory_locations USING btree (country_code);


--
-- Name: ix_inventory_locations_inventory_location_type_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_locations_inventory_location_type_id ON public.inventory_locations USING btree (inventory_location_type_id);


--
-- Name: ix_inventory_locations_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_locations_status ON public.inventory_locations USING btree (status);


--
-- Name: ix_inventory_movement_types_is_active; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_movement_types_is_active ON public.inventory_movement_types USING btree (is_active);


--
-- Name: ix_inventory_movements_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_movements_inventory_location_id ON public.inventory_movements USING btree (inventory_location_id);


--
-- Name: ix_inventory_movements_inventory_movement_type_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_movements_inventory_movement_type_id ON public.inventory_movements USING btree (inventory_movement_type_id);


--
-- Name: ix_inventory_movements_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_movements_item_id ON public.inventory_movements USING btree (item_id);


--
-- Name: ix_inventory_movements_occurred_at; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_inventory_movements_occurred_at ON public.inventory_movements USING btree (occurred_at);


--
-- Name: ix_item_partners_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_item_partners_partner_id ON public.item_partners USING btree (partner_id);


--
-- Name: ix_item_types_is_active; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_item_types_is_active ON public.item_types USING btree (is_active);


--
-- Name: ix_items_item_type_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_items_item_type_id ON public.items USING btree (item_type_id);


--
-- Name: ix_items_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_items_status ON public.items USING btree (status);


--
-- Name: ix_observation_decisions_decision_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_decisions_decision_id ON public.observation_decisions USING btree (decision_id);


--
-- Name: ix_observation_inbound_shipments_inbound_shipment_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_inbound_shipments_inbound_shipment_id ON public.observation_inbound_shipments USING btree (inbound_shipment_id);


--
-- Name: ix_observation_inventory_locations_inventory_location_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_inventory_locations_inventory_location_id ON public.observation_inventory_locations USING btree (inventory_location_id);


--
-- Name: ix_observation_inventory_movements_inventory_movement_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_inventory_movements_inventory_movement_id ON public.observation_inventory_movements USING btree (inventory_movement_id);


--
-- Name: ix_observation_items_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_items_item_id ON public.observation_items USING btree (item_id);


--
-- Name: ix_observation_partners_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_partners_partner_id ON public.observation_partners USING btree (partner_id);


--
-- Name: ix_observation_purchase_orders_purchase_order_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observation_purchase_orders_purchase_order_id ON public.observation_purchase_orders USING btree (purchase_order_id);


--
-- Name: ix_observations_observed_at; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_observations_observed_at ON public.observations USING btree (observed_at);


--
-- Name: ix_partner_types_is_active; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_partner_types_is_active ON public.partner_types USING btree (is_active);


--
-- Name: ix_partners_partner_type_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_partners_partner_type_id ON public.partners USING btree (partner_type_id);


--
-- Name: ix_partners_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_partners_status ON public.partners USING btree (status);


--
-- Name: ix_purchase_order_lines_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_purchase_order_lines_item_id ON public.purchase_order_lines USING btree (item_id);


--
-- Name: ix_purchase_order_lines_purchase_order_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_purchase_order_lines_purchase_order_id ON public.purchase_order_lines USING btree (purchase_order_id);


--
-- Name: ix_purchase_orders_order_date; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_purchase_orders_order_date ON public.purchase_orders USING btree (order_date);


--
-- Name: ix_purchase_orders_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_purchase_orders_partner_id ON public.purchase_orders USING btree (partner_id);


--
-- Name: ix_purchase_orders_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_purchase_orders_status ON public.purchase_orders USING btree (status);


--
-- Name: ix_sourcing_trip_decisions_decision_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trip_decisions_decision_id ON public.sourcing_trip_decisions USING btree (decision_id);


--
-- Name: ix_sourcing_trip_inbound_shipments_inbound_shipment_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trip_inbound_shipments_inbound_shipment_id ON public.sourcing_trip_inbound_shipments USING btree (inbound_shipment_id);


--
-- Name: ix_sourcing_trip_items_item_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trip_items_item_id ON public.sourcing_trip_items USING btree (item_id);


--
-- Name: ix_sourcing_trip_observations_observation_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trip_observations_observation_id ON public.sourcing_trip_observations USING btree (observation_id);


--
-- Name: ix_sourcing_trip_partners_partner_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trip_partners_partner_id ON public.sourcing_trip_partners USING btree (partner_id);


--
-- Name: ix_sourcing_trip_purchase_orders_purchase_order_id; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trip_purchase_orders_purchase_order_id ON public.sourcing_trip_purchase_orders USING btree (purchase_order_id);


--
-- Name: ix_sourcing_trips_start_date; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trips_start_date ON public.sourcing_trips USING btree (start_date);


--
-- Name: ix_sourcing_trips_status; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_sourcing_trips_status ON public.sourcing_trips USING btree (status);


--
-- Name: ix_units_of_measure_is_active; Type: INDEX; Schema: public; Owner: she_os_user
--

CREATE INDEX ix_units_of_measure_is_active ON public.units_of_measure USING btree (is_active);


--
-- Name: brand_decisions fk_brand_decisions_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_decisions
    ADD CONSTRAINT fk_brand_decisions_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_decisions fk_brand_decisions_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_decisions
    ADD CONSTRAINT fk_brand_decisions_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: brand_inbound_shipments fk_brand_inbound_shipments_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_inbound_shipments
    ADD CONSTRAINT fk_brand_inbound_shipments_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_inbound_shipments fk_brand_inbound_shipments_inbound_shipment_id_inbound__1ef5; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_inbound_shipments
    ADD CONSTRAINT fk_brand_inbound_shipments_inbound_shipment_id_inbound__1ef5 FOREIGN KEY (inbound_shipment_id) REFERENCES public.inbound_shipments(id);


--
-- Name: brand_initiatives fk_brand_initiatives_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_initiatives
    ADD CONSTRAINT fk_brand_initiatives_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_initiatives fk_brand_initiatives_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_initiatives
    ADD CONSTRAINT fk_brand_initiatives_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: brand_inventory_locations fk_brand_inventory_locations_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_inventory_locations
    ADD CONSTRAINT fk_brand_inventory_locations_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_inventory_locations fk_brand_inventory_locations_inventory_location_id_inve_bf65; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_inventory_locations
    ADD CONSTRAINT fk_brand_inventory_locations_inventory_location_id_inve_bf65 FOREIGN KEY (inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: brand_items fk_brand_items_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_items
    ADD CONSTRAINT fk_brand_items_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_items fk_brand_items_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_items
    ADD CONSTRAINT fk_brand_items_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: brand_observations fk_brand_observations_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_observations
    ADD CONSTRAINT fk_brand_observations_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_observations fk_brand_observations_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_observations
    ADD CONSTRAINT fk_brand_observations_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: brand_partners fk_brand_partners_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_partners
    ADD CONSTRAINT fk_brand_partners_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_partners fk_brand_partners_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_partners
    ADD CONSTRAINT fk_brand_partners_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: brand_purchase_orders fk_brand_purchase_orders_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_purchase_orders
    ADD CONSTRAINT fk_brand_purchase_orders_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_purchase_orders fk_brand_purchase_orders_purchase_order_id_purchase_orders; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_purchase_orders
    ADD CONSTRAINT fk_brand_purchase_orders_purchase_order_id_purchase_orders FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_orders(id);


--
-- Name: brand_sourcing_trips fk_brand_sourcing_trips_brand_id_brands; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_sourcing_trips
    ADD CONSTRAINT fk_brand_sourcing_trips_brand_id_brands FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: brand_sourcing_trips fk_brand_sourcing_trips_sourcing_trip_id_sourcing_trips; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.brand_sourcing_trips
    ADD CONSTRAINT fk_brand_sourcing_trips_sourcing_trip_id_sourcing_trips FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: decision_inbound_shipments fk_decision_inbound_shipments_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inbound_shipments
    ADD CONSTRAINT fk_decision_inbound_shipments_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: decision_inbound_shipments fk_decision_inbound_shipments_inbound_shipment_id_inbou_776d; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inbound_shipments
    ADD CONSTRAINT fk_decision_inbound_shipments_inbound_shipment_id_inbou_776d FOREIGN KEY (inbound_shipment_id) REFERENCES public.inbound_shipments(id);


--
-- Name: decision_inventory_locations fk_decision_inventory_locations_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inventory_locations
    ADD CONSTRAINT fk_decision_inventory_locations_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: decision_inventory_locations fk_decision_inventory_locations_inventory_location_id_i_2ef5; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inventory_locations
    ADD CONSTRAINT fk_decision_inventory_locations_inventory_location_id_i_2ef5 FOREIGN KEY (inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: decision_inventory_movements fk_decision_inventory_movements_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inventory_movements
    ADD CONSTRAINT fk_decision_inventory_movements_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: decision_inventory_movements fk_decision_inventory_movements_inventory_movement_id_i_7e1d; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_inventory_movements
    ADD CONSTRAINT fk_decision_inventory_movements_inventory_movement_id_i_7e1d FOREIGN KEY (inventory_movement_id) REFERENCES public.inventory_movements(id);


--
-- Name: decision_items fk_decision_items_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_items
    ADD CONSTRAINT fk_decision_items_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: decision_items fk_decision_items_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_items
    ADD CONSTRAINT fk_decision_items_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: decision_partners fk_decision_partners_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_partners
    ADD CONSTRAINT fk_decision_partners_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: decision_partners fk_decision_partners_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_partners
    ADD CONSTRAINT fk_decision_partners_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: decision_purchase_orders fk_decision_purchase_orders_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_purchase_orders
    ADD CONSTRAINT fk_decision_purchase_orders_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: decision_purchase_orders fk_decision_purchase_orders_purchase_order_id_purchase_orders; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.decision_purchase_orders
    ADD CONSTRAINT fk_decision_purchase_orders_purchase_order_id_purchase_orders FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_orders(id);


--
-- Name: field_notes fk_field_notes_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.field_notes
    ADD CONSTRAINT fk_field_notes_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: inbound_shipment_lines fk_inbound_shipment_lines_inbound_shipment_id_inbound_shipments; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipment_lines
    ADD CONSTRAINT fk_inbound_shipment_lines_inbound_shipment_id_inbound_shipments FOREIGN KEY (inbound_shipment_id) REFERENCES public.inbound_shipments(id);


--
-- Name: inbound_shipment_lines fk_inbound_shipment_lines_purchase_order_line_id_purcha_c044; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipment_lines
    ADD CONSTRAINT fk_inbound_shipment_lines_purchase_order_line_id_purcha_c044 FOREIGN KEY (purchase_order_line_id) REFERENCES public.purchase_order_lines(id);


--
-- Name: inbound_shipment_lines fk_inbound_shipment_lines_unit_of_measure_id_units_of_measure; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipment_lines
    ADD CONSTRAINT fk_inbound_shipment_lines_unit_of_measure_id_units_of_measure FOREIGN KEY (unit_of_measure_id) REFERENCES public.units_of_measure(id);


--
-- Name: inbound_shipments fk_inbound_shipments_destination_inventory_location_id__9800; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inbound_shipments
    ADD CONSTRAINT fk_inbound_shipments_destination_inventory_location_id__9800 FOREIGN KEY (destination_inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: initiative_decisions fk_initiative_decisions_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_decisions
    ADD CONSTRAINT fk_initiative_decisions_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: initiative_decisions fk_initiative_decisions_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_decisions
    ADD CONSTRAINT fk_initiative_decisions_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_inbound_shipments fk_initiative_inbound_shipments_inbound_shipment_id_inb_790d; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_inbound_shipments
    ADD CONSTRAINT fk_initiative_inbound_shipments_inbound_shipment_id_inb_790d FOREIGN KEY (inbound_shipment_id) REFERENCES public.inbound_shipments(id);


--
-- Name: initiative_inbound_shipments fk_initiative_inbound_shipments_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_inbound_shipments
    ADD CONSTRAINT fk_initiative_inbound_shipments_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_inventory_locations fk_initiative_inventory_locations_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_inventory_locations
    ADD CONSTRAINT fk_initiative_inventory_locations_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_inventory_locations fk_initiative_inventory_locations_inventory_location_id_fda9; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_inventory_locations
    ADD CONSTRAINT fk_initiative_inventory_locations_inventory_location_id_fda9 FOREIGN KEY (inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: initiative_items fk_initiative_items_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_items
    ADD CONSTRAINT fk_initiative_items_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_items fk_initiative_items_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_items
    ADD CONSTRAINT fk_initiative_items_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: initiative_observations fk_initiative_observations_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_observations
    ADD CONSTRAINT fk_initiative_observations_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_observations fk_initiative_observations_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_observations
    ADD CONSTRAINT fk_initiative_observations_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: initiative_partners fk_initiative_partners_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_partners
    ADD CONSTRAINT fk_initiative_partners_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_partners fk_initiative_partners_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_partners
    ADD CONSTRAINT fk_initiative_partners_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: initiative_purchase_orders fk_initiative_purchase_orders_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_purchase_orders
    ADD CONSTRAINT fk_initiative_purchase_orders_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_purchase_orders fk_initiative_purchase_orders_purchase_order_id_purchase_orders; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_purchase_orders
    ADD CONSTRAINT fk_initiative_purchase_orders_purchase_order_id_purchase_orders FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_orders(id);


--
-- Name: initiative_sourcing_trips fk_initiative_sourcing_trips_initiative_id_initiatives; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_sourcing_trips
    ADD CONSTRAINT fk_initiative_sourcing_trips_initiative_id_initiatives FOREIGN KEY (initiative_id) REFERENCES public.initiatives(id);


--
-- Name: initiative_sourcing_trips fk_initiative_sourcing_trips_sourcing_trip_id_sourcing_trips; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiative_sourcing_trips
    ADD CONSTRAINT fk_initiative_sourcing_trips_sourcing_trip_id_sourcing_trips FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: initiatives fk_initiatives_initiative_type_id_initiative_types; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.initiatives
    ADD CONSTRAINT fk_initiatives_initiative_type_id_initiative_types FOREIGN KEY (initiative_type_id) REFERENCES public.initiative_types(id);


--
-- Name: inventory_balances fk_inventory_balances_inventory_location_id_inventory_locations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_balances
    ADD CONSTRAINT fk_inventory_balances_inventory_location_id_inventory_locations FOREIGN KEY (inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: inventory_balances fk_inventory_balances_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_balances
    ADD CONSTRAINT fk_inventory_balances_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: inventory_balances fk_inventory_balances_unit_of_measure_id_units_of_measure; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_balances
    ADD CONSTRAINT fk_inventory_balances_unit_of_measure_id_units_of_measure FOREIGN KEY (unit_of_measure_id) REFERENCES public.units_of_measure(id);


--
-- Name: inventory_locations fk_inventory_locations_inventory_location_type_id_inven_927e; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_locations
    ADD CONSTRAINT fk_inventory_locations_inventory_location_type_id_inven_927e FOREIGN KEY (inventory_location_type_id) REFERENCES public.inventory_location_types(id);


--
-- Name: inventory_movements fk_inventory_movements_inbound_shipment_line_id_inbound_d454; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT fk_inventory_movements_inbound_shipment_line_id_inbound_d454 FOREIGN KEY (inbound_shipment_line_id) REFERENCES public.inbound_shipment_lines(id);


--
-- Name: inventory_movements fk_inventory_movements_inventory_location_id_inventory__da53; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT fk_inventory_movements_inventory_location_id_inventory__da53 FOREIGN KEY (inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: inventory_movements fk_inventory_movements_inventory_movement_type_id_inven_6059; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT fk_inventory_movements_inventory_movement_type_id_inven_6059 FOREIGN KEY (inventory_movement_type_id) REFERENCES public.inventory_movement_types(id);


--
-- Name: inventory_movements fk_inventory_movements_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT fk_inventory_movements_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: inventory_movements fk_inventory_movements_related_movement_id_inventory_movements; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT fk_inventory_movements_related_movement_id_inventory_movements FOREIGN KEY (related_movement_id) REFERENCES public.inventory_movements(id);


--
-- Name: inventory_movements fk_inventory_movements_unit_of_measure_id_units_of_measure; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.inventory_movements
    ADD CONSTRAINT fk_inventory_movements_unit_of_measure_id_units_of_measure FOREIGN KEY (unit_of_measure_id) REFERENCES public.units_of_measure(id);


--
-- Name: item_partners fk_item_partners_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.item_partners
    ADD CONSTRAINT fk_item_partners_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: item_partners fk_item_partners_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.item_partners
    ADD CONSTRAINT fk_item_partners_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: items fk_items_item_type_id_item_types; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT fk_items_item_type_id_item_types FOREIGN KEY (item_type_id) REFERENCES public.item_types(id);


--
-- Name: observation_decisions fk_observation_decisions_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_decisions
    ADD CONSTRAINT fk_observation_decisions_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: observation_decisions fk_observation_decisions_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_decisions
    ADD CONSTRAINT fk_observation_decisions_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_inbound_shipments fk_observation_inbound_shipments_inbound_shipment_id_in_0126; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inbound_shipments
    ADD CONSTRAINT fk_observation_inbound_shipments_inbound_shipment_id_in_0126 FOREIGN KEY (inbound_shipment_id) REFERENCES public.inbound_shipments(id);


--
-- Name: observation_inbound_shipments fk_observation_inbound_shipments_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inbound_shipments
    ADD CONSTRAINT fk_observation_inbound_shipments_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_inventory_locations fk_observation_inventory_locations_inventory_location_i_db03; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inventory_locations
    ADD CONSTRAINT fk_observation_inventory_locations_inventory_location_i_db03 FOREIGN KEY (inventory_location_id) REFERENCES public.inventory_locations(id);


--
-- Name: observation_inventory_locations fk_observation_inventory_locations_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inventory_locations
    ADD CONSTRAINT fk_observation_inventory_locations_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_inventory_movements fk_observation_inventory_movements_inventory_movement_i_754c; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inventory_movements
    ADD CONSTRAINT fk_observation_inventory_movements_inventory_movement_i_754c FOREIGN KEY (inventory_movement_id) REFERENCES public.inventory_movements(id);


--
-- Name: observation_inventory_movements fk_observation_inventory_movements_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_inventory_movements
    ADD CONSTRAINT fk_observation_inventory_movements_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_items fk_observation_items_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_items
    ADD CONSTRAINT fk_observation_items_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: observation_items fk_observation_items_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_items
    ADD CONSTRAINT fk_observation_items_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_partners fk_observation_partners_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_partners
    ADD CONSTRAINT fk_observation_partners_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_partners fk_observation_partners_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_partners
    ADD CONSTRAINT fk_observation_partners_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: observation_purchase_orders fk_observation_purchase_orders_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_purchase_orders
    ADD CONSTRAINT fk_observation_purchase_orders_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: observation_purchase_orders fk_observation_purchase_orders_purchase_order_id_purcha_5720; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.observation_purchase_orders
    ADD CONSTRAINT fk_observation_purchase_orders_purchase_order_id_purcha_5720 FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_orders(id);


--
-- Name: partners fk_partners_partner_type_id_partner_types; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT fk_partners_partner_type_id_partner_types FOREIGN KEY (partner_type_id) REFERENCES public.partner_types(id);


--
-- Name: purchase_order_lines fk_purchase_order_lines_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_order_lines
    ADD CONSTRAINT fk_purchase_order_lines_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: purchase_order_lines fk_purchase_order_lines_purchase_order_id_purchase_orders; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_order_lines
    ADD CONSTRAINT fk_purchase_order_lines_purchase_order_id_purchase_orders FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_orders(id);


--
-- Name: purchase_order_lines fk_purchase_order_lines_unit_of_measure_id_units_of_measure; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_order_lines
    ADD CONSTRAINT fk_purchase_order_lines_unit_of_measure_id_units_of_measure FOREIGN KEY (unit_of_measure_id) REFERENCES public.units_of_measure(id);


--
-- Name: purchase_orders fk_purchase_orders_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.purchase_orders
    ADD CONSTRAINT fk_purchase_orders_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: sourcing_trip_decisions fk_sourcing_trip_decisions_decision_id_decisions; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_decisions
    ADD CONSTRAINT fk_sourcing_trip_decisions_decision_id_decisions FOREIGN KEY (decision_id) REFERENCES public.decisions(id);


--
-- Name: sourcing_trip_decisions fk_sourcing_trip_decisions_sourcing_trip_id_sourcing_trips; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_decisions
    ADD CONSTRAINT fk_sourcing_trip_decisions_sourcing_trip_id_sourcing_trips FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: sourcing_trip_inbound_shipments fk_sourcing_trip_inbound_shipments_inbound_shipment_id__84f8; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_inbound_shipments
    ADD CONSTRAINT fk_sourcing_trip_inbound_shipments_inbound_shipment_id__84f8 FOREIGN KEY (inbound_shipment_id) REFERENCES public.inbound_shipments(id);


--
-- Name: sourcing_trip_inbound_shipments fk_sourcing_trip_inbound_shipments_sourcing_trip_id_sou_4690; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_inbound_shipments
    ADD CONSTRAINT fk_sourcing_trip_inbound_shipments_sourcing_trip_id_sou_4690 FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: sourcing_trip_items fk_sourcing_trip_items_item_id_items; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_items
    ADD CONSTRAINT fk_sourcing_trip_items_item_id_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: sourcing_trip_items fk_sourcing_trip_items_sourcing_trip_id_sourcing_trips; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_items
    ADD CONSTRAINT fk_sourcing_trip_items_sourcing_trip_id_sourcing_trips FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: sourcing_trip_observations fk_sourcing_trip_observations_observation_id_observations; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_observations
    ADD CONSTRAINT fk_sourcing_trip_observations_observation_id_observations FOREIGN KEY (observation_id) REFERENCES public.observations(id);


--
-- Name: sourcing_trip_observations fk_sourcing_trip_observations_sourcing_trip_id_sourcing_trips; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_observations
    ADD CONSTRAINT fk_sourcing_trip_observations_sourcing_trip_id_sourcing_trips FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: sourcing_trip_partners fk_sourcing_trip_partners_partner_id_partners; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_partners
    ADD CONSTRAINT fk_sourcing_trip_partners_partner_id_partners FOREIGN KEY (partner_id) REFERENCES public.partners(id);


--
-- Name: sourcing_trip_partners fk_sourcing_trip_partners_sourcing_trip_id_sourcing_trips; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_partners
    ADD CONSTRAINT fk_sourcing_trip_partners_sourcing_trip_id_sourcing_trips FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- Name: sourcing_trip_purchase_orders fk_sourcing_trip_purchase_orders_purchase_order_id_purc_2a23; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_purchase_orders
    ADD CONSTRAINT fk_sourcing_trip_purchase_orders_purchase_order_id_purc_2a23 FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_orders(id);


--
-- Name: sourcing_trip_purchase_orders fk_sourcing_trip_purchase_orders_sourcing_trip_id_sourc_906f; Type: FK CONSTRAINT; Schema: public; Owner: she_os_user
--

ALTER TABLE ONLY public.sourcing_trip_purchase_orders
    ADD CONSTRAINT fk_sourcing_trip_purchase_orders_sourcing_trip_id_sourc_906f FOREIGN KEY (sourcing_trip_id) REFERENCES public.sourcing_trips(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 8agZM3ifipFZ7MYwkrAeUbyT6L9Xce6Q7e9qAvVgmSI8Gus0XuMnagQRnfnYClZ

