from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.decision import DecisionCreate, DecisionRead, DecisionUpdate
from app.services import decision as decision_service
from app.services.decision import DecisionNotFoundError

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.get("", response_model=list[DecisionRead])
def list_decisions(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return decision_service.list_decisions(db, limit=limit, offset=offset)


@router.get("/{decision_id}", response_model=DecisionRead)
def get_decision(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return decision_service.get_decision(db, decision_id)
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("", response_model=DecisionRead, status_code=status.HTTP_201_CREATED)
def create_decision(payload: DecisionCreate, db: Session = Depends(get_db)):
    return decision_service.create_decision(db, payload)


@router.patch("/{decision_id}", response_model=DecisionRead)
def update_decision(
    decision_id: UUID,
    payload: DecisionUpdate,
    db: Session = Depends(get_db),
):
    try:
        return decision_service.update_decision(db, decision_id, payload)
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.delete("/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_decision(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        decision_service.delete_decision(db, decision_id)
    except DecisionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
