from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.repositories import brand as brand_repo
from app.schemas.brand import BrandCreate, BrandUpdate


class BrandNotFoundError(Exception):
    """No brand exists with the given identifier."""


class BrandSlugConflictError(Exception):
    """A brand with this slug already exists."""


class BrandNameConflictError(Exception):
    """A brand with this name already exists."""


def _raise_conflict(exc: IntegrityError, name: str | None, slug: str | None) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "slug" in constraint:
        raise BrandSlugConflictError(
            f"A brand with slug '{slug}' already exists"
        ) from exc
    if "name" in constraint:
        raise BrandNameConflictError(
            f"A brand with name '{name}' already exists"
        ) from exc
    raise


def get_brand(db: Session, brand_id: UUID) -> Brand:
    """Get a brand by its ID."""

    brand = brand_repo.get(db, brand_id)
    if brand is None:
        raise BrandNotFoundError(f"No brand found with ID {brand_id}")
    return brand


def list_brands(db: Session, limit: int = 100, offset: int = 0) -> list[Brand]:
    """List all brands."""

    return brand_repo.list_all(db, limit=limit, offset=offset)


def create_brand(db: Session, payload: BrandCreate) -> Brand:
    """Create a new brand."""

    brand = Brand(
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        status=payload.status,
    )

    try:
        brand = brand_repo.create(db, brand)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc, name=payload.name, slug=payload.slug)

    db.refresh(brand)
    return brand


def update_brand(db: Session, brand_id: UUID, payload: BrandUpdate) -> Brand:
    """Update an existing brand."""

    brand = get_brand(db, brand_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(brand, field, value)

    try:
        brand = brand_repo.update(db, brand)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            name=changes.get("name"),
            slug=changes.get("slug"),
        )

    db.refresh(brand)
    return brand


def delete_brand(db: Session, brand_id: UUID) -> None:
    """Delete a brand by its ID."""

    brand = get_brand(db, brand_id)
    brand_repo.delete(db, brand)
    db.commit()
