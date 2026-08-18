from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.partner import Partner


def get(db: Session, partner_id: UUID) -> Partner | None:
    return db.get(Partner, partner_id)


def get_by_slug(db: Session, slug: str) -> Partner | None:
    return db.scalar(select(Partner).where(Partner.slug == slug))


def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Partner]:
    return list(
        db.scalars(
            select(Partner).order_by(Partner.name).limit(limit).offset(offset)
        )
    )


def create(db: Session, partner: Partner) -> Partner:
    db.add(partner)
    db.flush()
    db.refresh(partner)
    return partner


def update(db: Session, partner: Partner) -> Partner:
    db.add(partner)
    db.flush()
    db.refresh(partner)
    return partner


def delete(db: Session, partner: Partner) -> None:
    db.delete(partner)
    db.flush()
