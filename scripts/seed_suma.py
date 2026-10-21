"""Seed the full operational slice for SUMA so the orrery can draw one brand completely.

Depth-first for SUMA only: partners, items, a warehouse, a sourcing trip,
observations, a decision, a purchase order + line, an inbound shipment + line,
and the receiving inventory movement, with the association links between them.

Idempotent: safe to re-run. Entities are matched by slug / title / number and
skipped if they already exist. The transactional tier (PO -> shipment -> movement)
is guarded by the PO number, so re-running will not double-post inventory.

Run with the API up on :8000, after seed_core.py:

    python scripts/seed_suma.py

Representative values. Replace copy / quantities with your real data as needed.
"""
import sys
import requests

BASE = "http://localhost:8000"

# ── stable lookup-type UUIDs (seeded by the Alembic lookup migrations) ──────────
IT_MATERIAL = "11111111-0000-4000-8000-000000000001"
IT_COMPONENT = "11111111-0000-4000-8000-000000000002"
IT_FINISHED = "11111111-0000-4000-8000-000000000004"
IT_PACKAGING = "11111111-0000-4000-8000-000000000005"
PT_SUPPLIER = "22222222-0000-4000-8000-000000000001"
PT_CRAFTER = "22222222-0000-4000-8000-000000000003"
PT_MANUFACTURER = "22222222-0000-4000-8000-000000000002"
PT_LOGISTICS = "22222222-0000-4000-8000-000000000007"
LT_WAREHOUSE = "44444444-0000-4000-8000-000000000001"
MT_RECEIPT = "55555555-0000-4000-8000-000000000001"
UOM_BUNDLE = "66666666-0000-4000-8000-000000000002"
UOM_PIECE = "66666666-0000-4000-8000-000000000001"


def die(msg: str) -> None:
    sys.exit(msg)


def find(path: str, key: str, value: str) -> dict | None:
    res = requests.get(f"{BASE}{path}", params={"limit": 500})
    res.raise_for_status()
    for row in res.json():
        if row.get(key) == value:
            return row
    return None


def ensure(path: str, payload: dict, key: str) -> dict:
    """Return the existing row (matched on key) or create it."""
    existing = find(path, key, payload[key])
    if existing:
        print(f"  exists  {path} :: {payload[key]}")
        return existing
    res = requests.post(f"{BASE}{path}", json=payload)
    if res.status_code == 201:
        print(f"  created {path} :: {payload[key]}")
        return res.json()
    if res.status_code == 409:
        again = find(path, key, payload[key])
        if again:
            return again
    die(f"  FAILED  {path} :: {payload[key]} -> {res.status_code} {res.text}")


def link(path: str) -> None:
    res = requests.post(f"{BASE}{path}")
    if res.status_code in (204, 409):
        print(f"  link    {path} ({res.status_code})")
    else:
        print(f"  LINK?   {path} -> {res.status_code} {res.text}")


def main() -> None:
    try:
        requests.get(f"{BASE}/brands", timeout=5).raise_for_status()
    except Exception as exc:
        die(f"API not reachable at {BASE} ({exc}). Start the backend first.")

    # ── 0 · anchors (created by seed_core.py) ──────────────────────────────────
    suma = find("/brands", "slug", "suma") or die("SUMA brand missing — run seed_core.py first.")
    editions = find("/initiatives", "slug", "editions")
    sid = suma["id"]
    print(f"SUMA = {sid}")

    # ── 1 · partners ───────────────────────────────────────────────────────────
    print("Partners...")
    # p_supplier = ensure("/partners", {
    #     "name": "Sanyuanli Hair Market", "slug": "sanyuanli_hair_market",
    #     "partner_type_id": PT_SUPPLIER, "status": "active",
    #     "description": "Guangzhou hair sourcing hub.",
    # }, "slug")
    p_crafter = ensure("/partners", {
        "name": "Nancy Nwachukwu", "slug": "nancy_nwachukwu",
        "partner_type_id": PT_CRAFTER, "status": "active",
        "description": "Hair shop owner, braider, and assistant in Abuja. Resides in Mpape, Nigeria. Manages a team of over 7 braiders, finishers, and ventilators.",
    }, "slug")
    p_mfr = ensure("/partners", {
        "name": "Outre X-Pression", "slug": "outre_xpression",
        "partner_type_id": PT_MANUFACTURER, "status": "inactive",
        "description": "Synthetic and protective-style hair manufacturer.",
    }, "slug")
    p_logi = ensure("/partners", {
        "name": "DHL Nigeria", "slug": "dhl_nigeria",
        "partner_type_id": PT_LOGISTICS, "status": "inactive",
        "description": "International logistics provider.",
    }, "slug")
    for p in (p_crafter, p_mfr, p_logi):
        link(f"/brands/{sid}/partners/{p['id']}")

    # ── 2 · items ──────────────────────────────────────────────────────────────
    print("Items...")
    i_hair = ensure("/items", {
        "name": "Human Hair Bundle 10in", "slug": "human_hair_bundle_10in",
        "sku": "SUMA-HHB-10", "item_type_id": IT_MATERIAL, "status": "active",
        "description": "Raw human hair bundle, 10 inch.",
    }, "slug")
    i_cap = ensure("/items", {
        "name": "Full Lace Cap", "slug": "full_lace_cap",
        "sku": "SUMA-FLC", "item_type_id": IT_COMPONENT, "status": "active",
        "description": "Full lace wig cap.",
    }, "slug")
    i_wig = ensure("/items", {
        "name": "Mutinta Licorice 10in", "slug": "mutinta_10in_licorice",
        "sku": "SUMA-MUT-10-LIC", "item_type_id": IT_FINISHED, "status": "active",
        "description": "Finished Mutinta wig, licorice, 10 inch.",
    }, "slug")
    i_box = ensure("/items", {
        "name": "SUMA Packaging Box", "slug": "suma_packaging_box",
        "sku": "SUMA-PKG-BOX", "item_type_id": IT_PACKAGING, "status": "inactive",
        "description": "Branded packaging box.",
    }, "slug")
    for it in (i_hair, i_cap, i_wig, i_box):
        link(f"/brands/{sid}/items/{it['id']}")
    link(f"/items/{i_hair['id']}/partners/{p_crafter['id']}")

    # ── 3 · inventory location ─────────────────────────────────────────────────
    print("Inventory location...")
    loc = ensure("/inventory-locations", {
        "inventory_location_type_id": LT_WAREHOUSE,
        "name": "Abuja Warehouse", "slug": "abuja_warehouse", "status": "active",
        "description": "Primary SUMA storage.",
        "address_line_1": "Lugbe", "city": "Abuja", "region": "FCT", "country_code": "NG",
    }, "slug")
    link(f"/brands/{sid}/inventory-locations/{loc['id']}")

    # ── 4 · sourcing trip ──────────────────────────────────────────────────────
    print("Sourcing trip...")
    trip = ensure("/sourcing-trips", {
        "name": "Oriental Spring 26", "slug": "oriental_spring_26", "status": "completed",
        "description": "China and Vietnam sourcing trip.",
        "start_date": "2026-05-08", "end_date": "2026-06-08",
    }, "slug")
    link(f"/brands/{sid}/sourcing-trips/{trip['id']}")
    link(f"/sourcing-trips/{trip['id']}/partners/{p_crafter['id']}")
    link(f"/sourcing-trips/{trip['id']}/items/{i_hair['id']}")

    # ── 5 · observations ───────────────────────────────────────────────────────
    print("Observations...")
    o_auto = ensure("/observations", {
        "title": "Automation interest in braiding tools",
        "details": "Growing industry interest in automation tools for braiding; a "
                   "clear opening for SUMA in the beauty-tech space. We should explore partnerships with braiding tool manufacturers and with robotics labs to develop a prototype braiding machine. A good place to start would be to reach out to the AI team from MUShanghai that presented their nail virtual try on tool at the 2026 spring conference.",
        "observed_at": "2026-10-20T09:30:00Z",
    }, "title")
    o_plant = ensure("/observations", {
        "title": "Plant-based braiding hair demand",
        "details": "Rising demand for plant-based, biodegradable braiding hair among "
                   "conscious consumers.",
        "observed_at": "2026-03-15T11:00:00Z",
    }, "title")
    for o in (o_auto, o_plant):
        link(f"/brands/{sid}/observations/{o['id']}")
    link(f"/sourcing-trips/{trip['id']}/observations/{o_plant['id']}")
    link(f"/observations/{o_plant['id']}/items/{i_hair['id']}")
    link(f"/observations/{o_plant['id']}/partners/{p_crafter['id']}")

    # ── 6 · decision ───────────────────────────────────────────────────────────
    print("Decision...")
    dec = ensure("/decisions", {
        "title": "Limit production runs to 500 units",
        "decision_summary": "Cap each SUMA production run at 500 units.",
        "reasoning": "Preserves small-batch quality and scarcity while managing cost risk.",
        "status": "in_effect", "decided_at": "2026-03-20T00:00:00Z",
    }, "title")
    link(f"/brands/{sid}/decisions/{dec['id']}")
    link(f"/decisions/{dec['id']}/items/{i_wig['id']}")
    link(f"/observations/{o_auto['id']}/decisions/{dec['id']}")

    # ── 7-9 · transactional tier (guarded by PO number) ────────────────────────
    print("Transactional tier (PO -> shipment -> movement)...")
    if find("/purchase-orders", "purchase_order_number", "SHE-PO-1001"):
        print("  SHE-PO-1001 exists — skipping transactional tier (already seeded).")
    else:
        po = requests.post(f"{BASE}/purchase-orders", json={
            "purchase_order_number": "SHE-PO-1001",
            "partner_id": p_crafter["id"], "status": "accepted",
            "order_date": "2026-03-14", "currency_code": "NGN",
            "brand_ids": [sid],
            "production_brief": "10 10in pieces of the Mutinta style.",
            "lines": [{
                "item_id": i_hair["id"], "quantity_ordered": 10,
                "unit_of_measure_id": UOM_PIECE,
                "description": "10in Mutinta wigs.",
            }],
        })
        if po.status_code != 201:
            die(f"  PO failed -> {po.status_code} {po.text}")
        po = po.json()
        po_line_id = po["lines"][0]["id"]
        print(f"  created PO {po['purchase_order_number']} (line {po_line_id})")

        ship = requests.post(f"{BASE}/inbound-shipments", json={
            "inbound_shipment_number": "SHE-IS-1001", "status": "received",
            "carrier_name": "DHL", "tracking_number": "1Z999AA10123456784",
            "destination_inventory_location_id": loc["id"],
            "shipped_at": "2026-04-28T10:00:00Z", "received_at": "2026-05-21T14:00:00Z",
            "brand_ids": [sid],
            "lines": [{
                "purchase_order_line_id": po_line_id, "quantity_shipped": 10,
                "unit_of_measure_id": UOM_PIECE,
            }],
        })
        if ship.status_code != 201:
            die(f"  shipment failed -> {ship.status_code} {ship.text}")
        ship = ship.json()
        ship_line_id = ship["lines"][0]["id"]
        print(f"  created shipment {ship['inbound_shipment_number']} (line {ship_line_id})")

        mv = requests.post(f"{BASE}/inventory-movements", json={
            "item_id": i_hair["id"], "inventory_location_id": loc["id"],
            "inventory_movement_type_id": MT_RECEIPT,
            "inbound_shipment_line_id": ship_line_id,
            "quantity_delta": 10, "unit_of_measure_id": UOM_PIECE,
            "occurred_at": "2026-05-21T14:00:00Z",
            "notes": "Received from Oriental Spring shipment.",
        })
        if mv.status_code != 201:
            die(f"  movement failed -> {mv.status_code} {mv.text}")
        print("  created receipt movement (+10 pieces at Abuja Warehouse)")

    # ── 10 · initiative link ───────────────────────────────────────────────────
    if editions:
        link(f"/brands/{sid}/initiatives/{editions['id']}")

    print("Done. SUMA is fully seeded.")


if __name__ == "__main__":    main()



{
  "name": "Nina Licorice 14in",
  "slug": "nina_4in_licorice",
  "sku": "SUMA-NINA-4-LIC",
  "item_type_id": "11111111-0000-4000-8000-000000000004",
  "description": "Finished Nina wig, licorice, 4 inch.",
  "status": "active"
}