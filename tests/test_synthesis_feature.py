from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database.deps import get_db
from app.main import app
from app.repositories import observation as observation_repo
from app.services.synthesis import NoObservationsError, synthesize_decision


def test_synthesize_decision_uses_tool_choice_and_maps_tool_output():
    observation_ids = [uuid4(), uuid4()]
    db = MagicMock()
    observations = [
        SimpleNamespace(id=observation_ids[0], details="First observation about supplier pricing."),
        SimpleNamespace(id=observation_ids[1], details="Second observation about vendor lead times."),
    ]
    with patch.object(observation_repo, "list_by_initiative", return_value=observations) as list_observations:
        client = MagicMock()
        client.messages.create.return_value = SimpleNamespace(
            content=[
                SimpleNamespace(
                    type="tool_use",
                    input={
                        "decision_summary": "Proceed with the proposed pilot.",
                        "reasoning": "The observations support the pilot with manageable lead-time risk.",
                        "confidence": " HIGH ",
                    },
                )
            ]
        )

        initiative_id = uuid4()
        response = synthesize_decision(
            db,
            initiative_id,
            client,
            model="claude-sonnet-5",
        )
        list_observations.assert_called_once_with(db, initiative_id)

        assert response.initiative_id == initiative_id
        assert response.observation_count == 2
        assert response.draft.decision_summary == "Proceed with the proposed pilot."
        assert response.draft.confidence == "high"
        assert response.draft.source_observation_ids == observation_ids
        assert response.draft.reasoning == "The observations support the pilot with manageable lead-time risk."

        create_call = client.messages.create.call_args.kwargs
        assert create_call["model"] == "claude-sonnet-5"
        assert create_call["tool_choice"] == {"type": "tool", "name": "draft_decision"}


def test_initiative_synthesis_route_success_and_404():
    initiative_id = uuid4()
    expected_response = {
        "initiative_id": str(initiative_id),
        "observation_count": 2,
        "draft": {
            "decision_summary": "Proceed with the pilot.",
            "reasoning": "Signal quality is strong enough to move forward.",
            "confidence": "medium",
            "source_observation_ids": [str(uuid4()), str(uuid4())],
        },
    }

    with patch("app.routers.synthesis.synthesis_service.synthesize_decision", return_value=expected_response) as mocked_service:
        app.dependency_overrides[get_db] = lambda: object()
        with TestClient(app) as client:
            response = client.post(f"/initiatives/{initiative_id}/synthesize")
            assert response.status_code == 200
            assert response.json() == expected_response
            mocked_service.assert_called_once()
            assert mocked_service.call_args.args[1] == initiative_id

    with patch("app.routers.synthesis.synthesis_service.synthesize_decision", side_effect=NoObservationsError("No observations available.")):
        app.dependency_overrides[get_db] = lambda: object()
        with TestClient(app) as client:
            response = client.post(f"/initiatives/{initiative_id}/synthesize")
            assert response.status_code == 404
            assert response.json()["detail"] == "No observations available."

    app.dependency_overrides.clear()
