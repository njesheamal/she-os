from app.main import app


def test_association_routes_present_in_openapi():
    paths = app.openapi().get("paths", {})

    assert "/brands/{brand_id}/items" in paths
    assert "/brands/{brand_id}/partners" in paths
    assert "/brands/{brand_id}/sourcing-trips" in paths
    assert "/initiatives/{initiative_id}/items" in paths
    assert "/sourcing-trips/{trip_id}/items" in paths
    assert "/observations/{observation_id}/decisions" in paths
    assert "/observations/{observation_id}/inventory-movements" in paths
    assert "/decisions/{decision_id}/items" in paths
    assert "/decisions/{decision_id}/inventory-movements" in paths
    assert "/items/{item_id}/partners" in paths
