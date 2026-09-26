---

# SHÉ OS — Project Shape Reference

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Driver | psycopg 3 (`postgresql+psycopg://`) |
| Database | PostgreSQL 16 (Docker) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Environment | GitHub Codespaces, `/workspaces/she-os` |

---

## File Layout

```
app/
  common.py                    — SLUG_PATTERN, COUNTRY_CODE_PATTERN, CURRENCY_CODE_PATTERN
  enums.py                     — all StrEnum status vocabularies
  main.py
  database/
    base.py
    constraints.py
    deps.py
    lookups.py
    mixins.py
    session.py
  models/
    __init__.py
    associations.py
    brand.py / decision.py / inbound_shipment.py / inbound_shipment_line.py
    initiative.py / inventory_balance.py / inventory_location.py
    inventory_movement.py / item.py / observation.py / partner.py
    purchase_order.py / purchase_order_line.py / sourcing_trip.py
  repositories/
    associations/
      __init__.py              — association repo functions live here
    brand.py / decision.py / inbound_shipment.py / initiative.py
    inventory_balance.py / inventory_location.py / inventory_movements.py
    item.py / observation.py / partner.py / purchase_order.py / sourcing_trip.py
  schemas/
    brand.py / decision.py / inbound_shipment.py / initiative.py
    inventory_balance.py / inventory_location.py / inventory_movement.py
    item.py / observation.py / partner.py / purchase_order.py
    sourcing_trip.py / synthesis.py
  services/
    associations/
      __init__.py
      brand_associations.py / decision_associations.py / initiative_associations.py
      item_associations.py / observation_associations.py / sourcing_trip_associations.py
    brand.py / decision.py / inbound_shipment.py / initiative.py
    inventory_location.py / inventory_movement.py / item.py
    observation.py / partner.py / purchase_order.py / sourcing_trip.py
    synthesis.py
  routers/
    associations/
      __init__.py
      brand_associations.py / decision_associations.py / initiative_associations.py
      item_associations.py / observation_associations.py / sourcing_trip_associations.py
    brand.py / decision.py / inbound_shipment.py / initiative.py
    inventory_location.py / inventory_movement.py / item.py
    observation.py / partner.py / purchase_order.py / sourcing_trip.py
    synthesis.py
tests/
  test_openapi_association_routes.py
  test_synthesis_feature.py
alembic/
  env.py / script.py.mako / README
  versions/
    bedf3037f156_create_initial_schema.py
    44f1b3c7682e_seed_lookup_values.py
    71605574e09c_add_publishing_initiative_type.py
    7ed26197f8a6_add_production_brief_to_purchase_orders.py
docs/
  DATABASE_DESIGN.md / DOMAIN_MODEL.md / DOMAIN_RELATIONSHIPS.md
  PHILOSOPHY.md / PRODUCT_VISION.md / ROADMAP.md / prompt.txt
backend/
  requirements.txt
docker-compose.yml

```

---

## The Five-Layer Pattern

Every entity follows this shape exactly, in this order:

```
Schema → Repository → Service → Router → main.py
```

| Layer | Job | Knows about |
|---|---|---|
| Schema | Wire shape, validation | Pydantic, enums |
| Repository | Read/write ORM objects | SQLAlchemy, database |
| Service | Business logic, owns commit | Repository, schemas |
| Router | HTTP translation | Service, schemas, status codes |
| `main.py` | Wires everything | Routers |

---

## Schema Shape

```python
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.enums import BrandStatus
from app.schemas.common import SLUG_PATTERN


class BrandBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
        examples=["SUMA"]
    )
    slug: str = Field(
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["suma"]
    )
    description: str | None = None
    status: BrandStatus


class BrandCreate(BrandBase):
    """What a client sends to create a brand."""


class BrandUpdate(BaseModel):
    """All fields optional."""
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["SUMA"]
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=SLUG_PATTERN,
        examples=["suma"]
    )
    description: str | None = None
    status: BrandStatus | None = None


class BrandRead(BrandBase):
    """What the API sends back."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
```

**Rules:**
- `Field()` — one argument per line, always
- `examples` on every field
- `from_attributes=True` on `Read` only
- `BrandUpdate` never inherits from `BrandBase` — all fields must be independently optional
- `status` is required on create (no default)

---

## Repository Shape

```python
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.brand import Brand


def get(db: Session, brand_id: UUID) -> Brand | None:
    return db.get(Brand, brand_id)

def get_by_slug(db: Session, slug: str) -> Brand | None:
    return db.scalar(select(Brand).where(Brand.slug == slug))

def list_all(db: Session, limit: int = 100, offset: int = 0) -> list[Brand]:
    return list(db.scalars(
        select(Brand).order_by(Brand.name).limit(limit).offset(offset)
    ))

def create(db: Session, brand: Brand) -> Brand:
    db.add(brand)
    db.flush()
    db.refresh(brand)
    return brand

def update(db: Session, brand: Brand) -> Brand:
    db.add(brand)
    db.flush()
    db.refresh(brand)
    return brand

def delete(db: Session, brand: Brand) -> None:
    db.delete(brand)
    db.flush()
```

**Rules:**
- `flush()` only — never `commit()` in a repository
- `refresh()` after flush so server-generated values populate
- Takes and returns ORM objects only — no schemas

---

## Service Shape

```python
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


def _raise_conflict(exc: IntegrityError, name=None, slug=None) -> None:
    diag = getattr(exc.orig, "diag", None)
    constraint = getattr(diag, "constraint_name", "") or ""
    if "slug" in constraint:
        raise BrandSlugConflictError(f"A brand with slug '{slug}' already exists") from exc
    if "name" in constraint:
        raise BrandNameConflictError(f"A brand with name '{name}' already exists") from exc
    raise


def get_brand(db: Session, brand_id: UUID) -> Brand:
    brand = brand_repo.get(db, brand_id)
    if brand is None:
        raise BrandNotFoundError(f"No brand found with ID {brand_id}")
    return brand


def create_brand(db: Session, payload: BrandCreate) -> Brand:
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
    brand = get_brand(db, brand_id)
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(brand, field, value)
    try:
        brand = brand_repo.update(db, brand)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        _raise_conflict(exc, name=changes.get("name"), slug=changes.get("slug"))
    db.refresh(brand)
    return brand


def delete_brand(db: Session, brand_id: UUID) -> None:
    brand = get_brand(db, brand_id)
    brand_repo.delete(db, brand)
    db.commit()
```

**Rules:**
- `commit()` lives here, never in the repository
- `rollback()` immediately after catching `IntegrityError`
- `_raise_conflict` reads `exc.orig.diag.constraint_name` — reliable because of the naming convention
- `exclude_unset=True` on `model_dump` for partial updates
- Explicit field assignment in constructors — never `Brand(**payload.model_dump())`

---

## Router Shape

```python
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.services import brand as brand_service
from app.services.brand import BrandNameConflictError, BrandNotFoundError, BrandSlugConflictError

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", response_model=list[BrandRead])
def list_brands(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return brand_service.list_brands(db, limit=limit, offset=offset)


@router.post("", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
def create_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    try:
        return brand_service.create_brand(db, payload)
    except (BrandSlugConflictError, BrandNameConflictError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.patch("/{brand_id}", response_model=BrandRead)
def update_brand(brand_id: UUID, payload: BrandUpdate, db: Session = Depends(get_db)):
    try:
        return brand_service.update_brand(db, brand_id, payload)
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (BrandSlugConflictError, BrandNameConflictError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        brand_service.delete_brand(db, brand_id)
    except BrandNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
```

**Rules:**
- Service imported as module alias (`brand_service`), exceptions imported by name
- `PATCH` not `PUT` — partial updates
- 201 on POST, 204 on DELETE (no body)
- FK violations → 422, unique conflicts → 409, not found → 404
- `/latest-number` routes declared **before** `/{id}` routes

---

## Status Codes

| Situation | Code |
|---|---|
| Created | 201 |
| No content (delete, link, unlink) | 204 |
| Not found | 404 |
| Unique constraint violation | 409 |
| FK violation / invalid reference | 422 |
| Balance would go negative | 409 |

---

## Swagger UI Examples

The absurd long decimal and garbage slug problems both come from missing `examples`. Every field must have one:

```python
# Slug — without examples, Swagger generates a 300-char regex match
slug: str = Field(
    min_length=1,
    max_length=255,
    pattern=SLUG_PATTERN,
    examples=["suma"]          # ← required to prevent garbage
)

# Decimal — send as string, no commas
quantity_ordered: Decimal = Field(
    gt=0,
    decimal_places=4,
    examples=["50.0000"]       # ← string, no comma separators
)

# Date vs datetime — always use full ISO 8601
occurred_at: datetime = Field(
    examples=["2026-05-21T14:00:00Z"]   # ← not "2026-05-21"
)

# Currency code
currency_code: str | None = Field(
    default=None,
    pattern=r"^[A-Z]{3}$",
    examples=["NGN"]
)

# Country code
country_code: str | None = Field(
    default=None,
    pattern=r"^[A-Z]{2}$",
    examples=["NG"]
)
```

**Known Swagger UI gotcha:** the Edit Value box caches the previous body. Use the **Reset** button before editing, or bypass entirely with curl for non-trivial payloads.

---

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Slugs | `snake_case` | `naija_new_year` |
| SKU (SHÉ-made) | `BRAND-STYLE-LENGTH-COLOR` | `SUMA-MUT-10-LIC` |
| SKU (purchased) | Supplier's own | whatever they give |
| PO numbers | `SHE-PO-1001` (4-digit, estate-wide) | `SHE-PO-1002` |
| IS numbers | `SHE-IS-1001` | `SHE-IS-1002` |
| Enums | `snake_case` values | `in_production` |
| Tables | `snake_case` plural | `purchase_order_lines` |
| URL paths | kebab-case | `/purchase-orders`, `/sourcing-trips` |

---

## Association Endpoint Shape

Every many-to-many gets exactly three endpoints:

```
GET    /{entity_a}/{id}/{entity_b_plural}           — list linked records
POST   /{entity_a}/{id}/{entity_b_plural}/{b_id}    — link (204)
DELETE /{entity_a}/{id}/{entity_b_plural}/{b_id}    — unlink (204)
```

No request body on POST or DELETE. Both IDs come from the URL.

---

## Shared Constants (`app/schemas/common.py`)

```python
SLUG_PATTERN = r"^[a-z0-9]+(_[a-z0-9]+)*$"
COUNTRY_CODE_PATTERN = r"^[A-Z]{2}$"
CURRENCY_CODE_PATTERN = r"^[A-Z]{3}$"
```

---

## Inventory Rules

| Rule | Where enforced |
|---|---|
| Balances only change via movements | Service layer |
| No update or delete on movements | No endpoints exist |
| No write endpoints on balances | No endpoints exist |
| Negative delta pre-checked before posting | Service, before commit |
| Balance upsert is atomic | `INSERT ... ON CONFLICT DO UPDATE` |


