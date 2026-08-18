from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.repositories import partner as partner_repo
from app.schemas.partner import PartnerCreate, PartnerUpdate


class PartnerNotFoundError(Exception):
    """No partner exists with the given identifier."""


class PartnerSlugConflictError(Exception):
    """A partner with this slug already exists."""


class PartnerTypeNotFoundError(Exception):
    """The referenced partner type does not exist."""


def _raise_conflict(
    exc: IntegrityError,
    slug: str | None,
    partner_type_id: UUID | None,
) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "slug" in constraint:
        raise PartnerSlugConflictError(
            f"A partner with slug '{slug}' already exists"
        ) from exc
    if "partner_type_id" in constraint:
        raise PartnerTypeNotFoundError(
            f"No partner type found with ID {partner_type_id}"
        ) from exc
    raise


def get_partner(db: Session, partner_id: UUID) -> Partner:
    partner = partner_repo.get(db, partner_id)
    if partner is None:
        raise PartnerNotFoundError(f"No partner found with ID {partner_id}")
    return partner


def list_partners(db: Session, limit: int = 100, offset: int = 0) -> list[Partner]:
    return partner_repo.list_all(db, limit=limit, offset=offset)


def create_partner(db: Session, payload: PartnerCreate) -> Partner:
    partner = Partner(
        name=payload.name,
        slug=payload.slug,
        partner_type_id=payload.partner_type_id,
        description=payload.description,
        status=payload.status,
        website=payload.website,
        email=payload.email,
        phone=payload.phone,
    )

    try:
        partner = partner_repo.create(db, partner)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=payload.slug,
            partner_type_id=payload.partner_type_id,
        )

    db.refresh(partner)
    return partner


def update_partner(
    db: Session, partner_id: UUID, payload: PartnerUpdate
) -> Partner:
    partner = get_partner(db, partner_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(partner, field, value)

    try:
        partner = partner_repo.update(db, partner)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=changes.get("slug"),
            partner_type_id=changes.get("partner_type_id"),
        )

    db.refresh(partner)
    return partner


def delete_partner(db: Session, partner_id: UUID) -> None:
    partner = get_partner(db, partner_id)
    partner_repo.delete(db, partner)
    db.commit()
