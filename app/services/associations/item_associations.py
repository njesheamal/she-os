from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.associations import item_partners
from app.models.item import Item
from app.models.partner import Partner
from app.repositories import item as item_repo
from app.repositories import partner as partner_repo
from app.schemas.partner import PartnerRead
from app.services.item import ItemNotFoundError
from app.services.partner import PartnerNotFoundError


class AlreadyLinkedError(Exception):
    pass


class NotLinkedError(Exception):
    pass


def list_partners_for_item(db: Session, item_id: UUID) -> list[Partner]:
    item = item_repo.get(db, item_id)
    if item is None:
        raise ItemNotFoundError(f"No item found with ID {item_id}")
    return list(
        db.scalars(
            Partner.__table__.select()
            .join(item_partners, item_partners.c.partner_id == Partner.id)
            .where(item_partners.c.item_id == item_id)
        )
    )


def link_partner_to_item(db: Session, item_id: UUID, partner_id: UUID) -> None:
    item = item_repo.get(db, item_id)
    if item is None:
        raise ItemNotFoundError(f"No item found with ID {item_id}")
    partner = partner_repo.get(db, partner_id)
    if partner is None:
        raise PartnerNotFoundError(f"No partner found with ID {partner_id}")
    try:
        db.execute(
            item_partners.insert().values(
                item_id=item_id,
                partner_id=partner_id,
            )
        )
        db.flush()
    except IntegrityError as exc:
        raise AlreadyLinkedError(
            f"Item {item_id} is already linked to partner {partner_id}"
        ) from exc


def unlink_partner_from_item(db: Session, item_id: UUID, partner_id: UUID) -> bool:
    item = item_repo.get(db, item_id)
    if item is None:
        raise ItemNotFoundError(f"No item found with ID {item_id}")
    result = db.execute(
        delete(item_partners).where(
            item_partners.c.item_id == item_id,
            item_partners.c.partner_id == partner_id,
        )
    )
    db.flush()
    if result.rowcount == 0:
        raise NotLinkedError(
            f"Item {item_id} is not linked to partner {partner_id}"
        )
    return True
