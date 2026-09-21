from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.brand import Brand

def get(db: Session, brand_id: UUID) -> Brand | None:
    """Get a brand by its ID."""
    return db.get(Brand, brand_id)

def get_by_slug(db: Session, slug: str) -> Brand | None:
    """Get a brand by its slug."""
    return db.scalar(select(Brand).where(Brand.slug == slug))

def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Brand]:
    """List all brands, with optional limit and offset."""
    return list(
    db.scalars(
            select(Brand)
            .order_by(Brand.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
    )

def create(db: Session, brand: Brand) -> Brand:
    """Create a new brand."""
    db.add(brand)
    db.flush()
    db.refresh(brand)
    return brand

def update(db: Session, brand: Brand) -> Brand:
    """Update an existing brand."""
    db.add(brand)
    db.flush()
    db.refresh(brand)
    return brand

def delete(db: Session, brand: Brand) -> None:
    """Delete a brand."""
    db.delete(brand)
    db.flush()