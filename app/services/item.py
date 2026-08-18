from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.item import Item
from app.repositories import item as item_repo
from app.schemas.item import ItemCreate, ItemUpdate


class ItemNotFoundError(Exception):
    """No item exists with the given identifier."""


class ItemSlugConflictError(Exception):
    """An item with this slug already exists."""


class ItemSkuConflictError(Exception):
    """An item with this SKU already exists."""


class ItemTypeNotFoundError(Exception):
    """The referenced item type does not exist."""


def _raise_conflict(
    exc: IntegrityError,
    slug: str | None,
    sku: str | None,
    item_type_id: UUID | None,
) -> None:
    """Translate a database constraint violation into a domain error."""
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""

    if "item_type_id" in constraint:
        raise ItemTypeNotFoundError(
            f"No item type found with ID {item_type_id}"
        ) from exc
    if "slug" in constraint:
        raise ItemSlugConflictError(
            f"An item with slug '{slug}' already exists"
        ) from exc
    if "sku" in constraint:
        raise ItemSkuConflictError(
            f"An item with SKU '{sku}' already exists"
        ) from exc
    raise


def get_item(db: Session, item_id: UUID) -> Item:
    item = item_repo.get(db, item_id)
    if item is None:
        raise ItemNotFoundError(f"No item found with ID {item_id}")
    return item


def list_items(db: Session, limit: int = 100, offset: int = 0) -> list[Item]:
    return item_repo.list_all(db, limit=limit, offset=offset)


def create_item(db: Session, payload: ItemCreate) -> Item:
    item = Item(
        name=payload.name,
        slug=payload.slug,
        sku=payload.sku,
        item_type_id=payload.item_type_id,
        description=payload.description,
        status=payload.status,
    )

    try:
        item = item_repo.create(db, item)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=payload.slug,
            sku=payload.sku,
            item_type_id=payload.item_type_id,
        )

    db.refresh(item)
    return item


def update_item(db: Session, item_id: UUID, payload: ItemUpdate) -> Item:
    item = get_item(db, item_id)

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(item, field, value)

    try:
        item = item_repo.update(db, item)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(
            exc,
            slug=changes.get("slug"),
            sku=changes.get("sku"),
            item_type_id=changes.get("item_type_id"),
        )

    db.refresh(item)
    return item


def delete_item(db: Session, item_id: UUID) -> None:
    item = get_item(db, item_id)
    item_repo.delete(db, item)
    db.commit()