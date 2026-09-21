from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.partner import PartnerRead
from app.services.associations import item_associations as assoc_service
from app.services.item import ItemNotFoundError
from app.services.partner import PartnerNotFoundError

router = APIRouter(prefix="/items", tags=["item associations"])


@router.get("/{item_id}/partners", response_model=list[PartnerRead])
def list_item_partners(item_id: UUID, db: Session = Depends(get_db)):
    try:
        return [PartnerRead.model_validate(p) for p in assoc_service.list_partners_for_item(db, item_id)]
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{item_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def link_item_partner(item_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.link_partner_to_item(db, item_id, partner_id)
        db.commit()
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except PartnerNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.AlreadyLinkedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{item_id}/partners/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_item_partner(item_id: UUID, partner_id: UUID, db: Session = Depends(get_db)):
    try:
        assoc_service.unlink_partner_from_item(db, item_id, partner_id)
        db.commit()
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except assoc_service.NotLinkedError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
