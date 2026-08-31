from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.observation import (
    ObservationCreate,
    ObservationRead,
    ObservationUpdate,
)
from app.services import observation as observation_service
from app.services.observation import ObservationNotFoundError

router = APIRouter(prefix="/observations", tags=["observations"])


@router.get("", response_model=list[ObservationRead])
def list_observations(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return observation_service.list_observations(
        db, limit=limit, offset=offset
    )


@router.get("/{observation_id}", response_model=ObservationRead)
def get_observation(observation_id: UUID, db: Session = Depends(get_db)):
    try:
        return observation_service.get_observation(db, observation_id)
    except ObservationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "", response_model=ObservationRead, status_code=status.HTTP_201_CREATED
)
def create_observation(
    payload: ObservationCreate, db: Session = Depends(get_db)
):
    return observation_service.create_observation(db, payload)


@router.patch("/{observation_id}", response_model=ObservationRead)
def update_observation(
    observation_id: UUID,
    payload: ObservationUpdate,
    db: Session = Depends(get_db),
):
    try:
        return observation_service.update_observation(
            db, observation_id, payload
        )
    except ObservationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.delete("/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_observation(observation_id: UUID, db: Session = Depends(get_db)):
    try:
        observation_service.delete_observation(db, observation_id)
    except ObservationNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
