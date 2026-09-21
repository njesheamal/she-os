from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.observation import Observation


def get(db: Session, observation_id: UUID) -> Observation | None:
    return db.get(Observation, observation_id)


def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Observation]:
    return list(
        db.scalars(
            select(Observation)
            .order_by(Observation.observed_at.desc().nullslast())
            .limit(limit)
            .offset(offset)
        )
    )


def create(db: Session, observation: Observation) -> Observation:
    db.add(observation)
    db.flush()
    db.refresh(observation)
    return observation


def update(db: Session, observation: Observation) -> Observation:
    db.add(observation)
    db.flush()
    db.refresh(observation)
    return observation


def delete(db: Session, observation: Observation) -> None:
    db.delete(observation)
    db.flush()
