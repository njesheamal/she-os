from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.decision import Decision


def get(db: Session, decision_id: UUID) -> Decision | None:
    return db.get(Decision, decision_id)


def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Decision]:
    return list(
        db.scalars(
            select(Decision)
            .order_by(Decision.decided_at.desc().nullslast(), Decision.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
    )


def create(db: Session, decision: Decision) -> Decision:
    db.add(decision)
    db.flush()
    db.refresh(decision)
    return decision


def update(db: Session, decision: Decision) -> Decision:
    db.add(decision)
    db.flush()
    db.refresh(decision)
    return decision


def delete(db: Session, decision: Decision) -> None:
    db.delete(decision)
    db.flush()
