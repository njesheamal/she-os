from uuid import UUID

from anthropic import Anthropic
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.database.session import ANTHROPIC_API, ANTHROPIC_MODEL
from app.schemas.synthesis import SynthesisResponse
from app.services import synthesis as synthesis_service
from app.services.synthesis import NoObservationsError, SynthesisError

router = APIRouter(prefix="/initiatives", tags=["initiative synthesis"])


def get_anthropic_client() -> Anthropic:
    return Anthropic(api_key=ANTHROPIC_API)


@router.post(
    "/{initiative_id}/synthesize",
    response_model=SynthesisResponse,
    responses={404: {"description": "No observations for this initiative"}},
)
def synthesize_initiative_decision(
    initiative_id: UUID,
    db: Session = Depends(get_db),
    client: Anthropic = Depends(get_anthropic_client),
):
    try:
        return synthesis_service.synthesize_decision(
            db,
            initiative_id,
            client,
            model=ANTHROPIC_MODEL,
        )
    except NoObservationsError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except SynthesisError as exc:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, str(exc)) from exc
