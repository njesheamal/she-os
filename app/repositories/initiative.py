from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.initiative import Initiative


def get(db: Session, initiative_id: UUID) -> Initiative | None:
    return db.get(Initiative, initiative_id)


def get_by_slug(db: Session, slug: str) -> Initiative | None:
    return db.scalar(select(Initiative).where(Initiative.slug == slug))


def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Initiative]:
    return list(
        db.scalars(
            select(Initiative).order_by(Initiative.name).limit(limit).offset(offset)
        )
    )


def create(db: Session, initiative: Initiative) -> Initiative:
    db.add(initiative)
    db.flush()
    db.refresh(initiative)
    return initiative


def update(db: Session, initiative: Initiative) -> Initiative:
    db.add(initiative)
    db.flush()
    db.refresh(initiative)
    return initiative


def delete(db: Session, initiative: Initiative) -> None:
    db.delete(initiative)
    db.flush()
