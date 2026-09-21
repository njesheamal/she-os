from uuid import UUID

from sqlalchemy.orm import Session

from app.models.decision import Decision
from app.repositories import decision as decision_repo
from app.schemas.decision import DecisionCreate, DecisionUpdate


class DecisionNotFoundError(Exception):
    """No decision exists with the given identifier."""


def get_decision(db: Session, decision_id: UUID) -> Decision:
    decision = decision_repo.get(db, decision_id)
    if decision is None:
        raise DecisionNotFoundError(
            f"No decision found with ID {decision_id}"
        )
    return decision


def list_decisions(
    db: Session, limit: int = 100, offset: int = 0
) -> list[Decision]:
    return decision_repo.list_all(db, limit=limit, offset=offset)


def create_decision(db: Session, payload: DecisionCreate) -> Decision:
    decision = Decision(
        title=payload.title,
        decision_summary=payload.decision_summary,
        reasoning=payload.reasoning,
        status=payload.status,
        decided_at=payload.decided_at,
    )
    decision = decision_repo.create(db, decision)
    db.commit()
    db.refresh(decision)
    return decision


def update_decision(
    db: Session, decision_id: UUID, payload: DecisionUpdate
) -> Decision:
    decision = get_decision(db, decision_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(decision, field, value)

    decision = decision_repo.update(db, decision)
    db.commit()
    db.refresh(decision)
    return decision


def delete_decision(db: Session, decision_id: UUID) -> None:
    decision = get_decision(db, decision_id)
    decision_repo.delete(db, decision)
    db.commit()
