from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.initiative import Initiative
from app.repositories import initiative as initiative_repo
from app.schemas.initiative import InitiativeCreate, InitiativeUpdate


class InitiativeNotFoundError(Exception):
    """No initiative exists with the given identifier."""


class InitiativeSlugConflictError(Exception):
    """An initiative with this slug already exists."""


class InitiativeTypeNotFoundError(Exception):
    """The referenced initiative type does not exist."""


class InitiativeDateRangeError(Exception):
    """The end date occurs before the start date."""


def _raise_conflict(
    exc: IntegrityError,
    slug: str | None,
    initiative_type_id: UUID | None,
) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "initiative_type_id" in constraint:
        raise InitiativeTypeNotFoundError(
            f"No initiative type found with ID {initiative_type_id}"
        ) from exc
    if "slug" in constraint:
        raise InitiativeSlugConflictError(
            f"An initiative with slug '{slug}' already exists"
        ) from exc
    if "dates_ordered" in constraint:
        raise InitiativeDateRangeError(
            "end_date must not occur before start_date"
        ) from exc
    raise


def get_initiative(db: Session, initiative_id: UUID) -> Initiative:
    initiative = initiative_repo.get(db, initiative_id)
    if initiative is None:
        raise InitiativeNotFoundError(
            f"No initiative found with ID {initiative_id}"
        )
    return initiative


def list_initiatives(
    db: Session, limit: int = 100, offset: int = 0
) -> list[Initiative]:
    return initiative_repo.list_all(db, limit=limit, offset=offset)


def create_initiative(db: Session, payload: InitiativeCreate) -> Initiative:
    initiative = Initiative(
        initiative_type_id=payload.initiative_type_id,
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        status=payload.status,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )

    try:
        initiative = initiative_repo.create(db, initiative)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=payload.slug,
            initiative_type_id=payload.initiative_type_id,
        )

    db.refresh(initiative)
    return initiative


def update_initiative(
    db: Session, initiative_id: UUID, payload: InitiativeUpdate
) -> Initiative:
    initiative = get_initiative(db, initiative_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(initiative, field, value)

    try:
        initiative = initiative_repo.update(db, initiative)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=changes.get("slug"),
            initiative_type_id=changes.get("initiative_type_id"),
        )

    db.refresh(initiative)
    return initiative


def delete_initiative(db: Session, initiative_id: UUID) -> None:
    initiative = get_initiative(db, initiative_id)
    initiative_repo.delete(db, initiative)
    db.commit()
