from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item


def get(db: Session, item_id: UUID) -> Item | None:
    return db.get(Item, item_id)


def get_by_slug(db: Session, slug: str) -> Item | None:
    return db.scalar(select(Item).where(Item.slug == slug))


def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Item]:
    return list(
        db.scalars(select(Item).order_by(Item.name).limit(limit).offset(offset))
    )


def create(db: Session, item: Item) -> Item:
    db.add(item)
    db.flush()
    db.refresh(item)
    return item


def update(db: Session, item: Item) -> Item:
    db.add(item)
    db.flush()
    db.refresh(item)
    return item


def delete(db: Session, item: Item) -> None:
    db.delete(item)
    db.flush()
