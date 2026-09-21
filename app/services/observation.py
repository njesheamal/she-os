from uuid import UUID

from sqlalchemy.orm import Session

from app.models.observation import Observation
from app.repositories import observation as observation_repo
from app.schemas.observation import ObservationCreate, ObservationUpdate


class ObservationNotFoundError(Exception):
    """No observation exists with the given identifier."""


def get_observation(db: Session, observation_id: UUID) -> Observation:
    observation = observation_repo.get(db, observation_id)
    if observation is None:
        raise ObservationNotFoundError(
            f"No observation found with ID {observation_id}"
        )
    return observation


def list_observations(
    db: Session, limit: int = 100, offset: int = 0
) -> list[Observation]:
    return observation_repo.list_all(db, limit=limit, offset=offset)


def create_observation(
    db: Session, payload: ObservationCreate
) -> Observation:
    observation = Observation(
        title=payload.title,
        details=payload.details,
        observed_at=payload.observed_at,
    )
    observation = observation_repo.create(db, observation)
    db.commit()
    db.refresh(observation)
    return observation


def update_observation(
    db: Session, observation_id: UUID, payload: ObservationUpdate
) -> Observation:
    observation = get_observation(db, observation_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(observation, field, value)

    observation = observation_repo.update(db, observation)
    db.commit()
    db.refresh(observation)
    return observation


def delete_observation(db: Session, observation_id: UUID) -> None:
    observation = get_observation(db, observation_id)
    observation_repo.delete(db, observation)
    db.commit()
