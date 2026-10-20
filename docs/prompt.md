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


<!--
GOAL
Add a "Field Notes" resource to SHÉ OS: publishable visual essays with full CRUD.
Follow the project's five-layer pattern (Schema -> Repository -> Service ->
Router -> main.py) exactly. No AI, no embeddings, no associations, no file
uploads, no frontend in this chunk.

A Field Note has two parts:
  Part one (required): the visual essay. A poem plus its imagery (media).
  Part two (optional): an in-depth essay. The deeper write-up, absent on a
    poem-only note.
Physical layout varies per note and is decided by the front end. The schema
stores the parts and their materials; it must NOT encode any fixed arrangement.

READ FIRST, THEN MIRROR (copy style, do not invent)
- Full "decision" resource: app/models/decision.py, app/schemas/decision.py,
  app/repositories/decision.py, app/services/decision.py, app/routers/decision.py
- "brand" for the slug + unique-conflict path: app/services/brand.py
  (_raise_conflict) and app/routers/brand.py (409 handling)
- app/enums.py, app/common.py, app/database/base.py, app/database/mixins.py,
  app/database/constraints.py (status_in), app/database/deps.py (get_db)
- A model with a nullable FK, to copy the initiative_id import/declaration exactly
- Any model already using a JSON/JSONB column; if one exists, match its import and
  mapped_column style. If none exists, use
  `from sqlalchemy.dialects.postgresql import JSONB`.
- alembic/env.py and versions/bedf3037f156_create_initial_schema.py for table style

IMPORTS (exact)
- from app.common import SLUG_PATTERN
- from app.database.constraints import status_in
- from app.database.base import Base
- from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
- from app.enums import FieldNoteStatus, MediaKind
- from sqlalchemy.dialects.postgresql import JSONB   (unless the codebase imports it elsewhere; then match)

ENUMS  app/enums.py  (UPPER name / lower value, house style)
  class FieldNoteStatus(StrEnum):
      DRAFT = "draft"
      PUBLISHED = "published"

  class MediaKind(StrEnum):
      IMAGE = "image"
      GIF = "gif"
      VIDEO = "video"
FieldNoteStatus is used for validation and the check constraint only. Status is
stored as String(20) + CheckConstraint, NOT a native pg enum (match decision.py).

MODEL  app/models/field_note.py  (declare only own columns; mixins supply id +
timestamps via sort_order)
  class FieldNote(UUIDPrimaryKeyMixin, TimestampMixin, Base):
      __tablename__ = "field_notes"
  Columns in order:
  - slug:   String(255), unique=True, index=True, nullable=False
  - title:  String(255), nullable=False
  - status: String(20), nullable=False, index=True   (default set in service, no server_default)
  - theme:  String(255), nullable=True
  - poem:   Text, nullable=False                      # part one, required
  - media:  JSONB, nullable=True                      # part one imagery; list of media refs
            Mapped[list[dict] | None]
  - essay:  Text, nullable=True                       # part two, optional
  - excerpt: String(500), nullable=True               # preview pull; not auto-derived
  - initiative_id: nullable UUID FK -> initiatives.id (copy a nullable FK you read)
  - published_at: DateTime(timezone=True), index=True, nullable=True
  __table_args__:
  - CheckConstraint("title <> ''", name="title_not_empty")
  - CheckConstraint("poem <> ''",  name="poem_not_empty")
  - CheckConstraint(status_in(FieldNoteStatus), name="status_valid")

SCHEMA  app/schemas/field_note.py  (match decision.py: no examples; from_attributes
on Read only; Update does not inherit Base). Field Notes differs from decision: it
has a slug (needs pattern) and status is NOT client-settable (Read only).

  class MediaRef(BaseModel):
      url: str = Field(min_length=1)
      kind: MediaKind
      alt: str | None = None
      caption: str | None = None

  class FieldNoteBase(BaseModel):
      title: str = Field(min_length=1, max_length=255)
      slug: str = Field(min_length=1, max_length=255, pattern=SLUG_PATTERN)
      theme: str | None = None
      poem: str = Field(min_length=1)                 # part one required
      media: list[MediaRef] | None = None
      essay: str | None = None                        # part two optional
      excerpt: str | None = Field(default=None, max_length=500)

  class FieldNoteCreate(FieldNoteBase):
      """Always created as a draft."""

  class FieldNoteUpdate(BaseModel):
      title: str | None = Field(default=None, min_length=1, max_length=255)
      slug: str | None = Field(default=None, min_length=1, max_length=255, pattern=SLUG_PATTERN)
      theme: str | None = None
      poem: str | None = Field(default=None, min_length=1)
      media: list[MediaRef] | None = None
      essay: str | None = None
      excerpt: str | None = Field(default=None, max_length=500)
      # no status here; status changes only via /publish

  class FieldNoteRead(FieldNoteBase):
      model_config = ConfigDict(from_attributes=True)
      id: UUID
      status: FieldNoteStatus
      published_at: datetime | None = None
      created_at: datetime
      updated_at: datetime

REPOSITORY  app/repositories/field_note.py  (flush() only, never commit; refresh
after flush; ORM in/out)
  get(db, field_note_id), get_by_slug(db, slug),
  list_all(db, status=None, limit=100, offset=0) ordered created_at desc, filtered
  by status when provided, create, update, delete

SERVICE  app/services/field_note.py  (commit here; rollback on IntegrityError;
explicit field assignment, never Model(**model_dump()))
  Exceptions: FieldNoteNotFoundError, FieldNoteSlugConflictError
  _raise_conflict: copy brand's, reading exc.orig.diag.constraint_name for "slug"
  create_field_note:
      note = FieldNote(
          slug=payload.slug, title=payload.title, status=FieldNoteStatus.DRAFT,
          theme=payload.theme, poem=payload.poem,
          media=[m.model_dump() for m in payload.media] if payload.media else None,
          essay=payload.essay, excerpt=payload.excerpt,
      )
      commit; on IntegrityError rollback + _raise_conflict(slug=payload.slug)
  update_field_note: get; changes = payload.model_dump(exclude_unset=True) (nested
      MediaRef serializes to list[dict] automatically); setattr loop; commit; same
      slug-conflict handling
  publish_field_note: status=FieldNoteStatus.PUBLISHED; set published_at only if
      currently None; commit; return note. Idempotent (re-publish returns 200,
      published_at unchanged)
  get_field_note (raises NotFound), list_field_notes, delete_field_note

ROUTER  app/routers/field_note.py  (prefix "/field-notes", tags=["field-notes"];
service as module alias, exceptions by name)
  GET    ""              list[FieldNoteRead]; Query status (FieldNoteStatus|None),
                         limit (ge=1, le=500, default 100), offset (ge=0, default 0)
  POST   ""              FieldNoteRead 201; slug conflict 409; bad FK 422
  GET    "/{id}"         FieldNoteRead; 404
  PATCH  "/{id}"         FieldNoteRead; 404; slug conflict 409; bad FK 422
  POST   "/{id}/publish" FieldNoteRead; 404
  DELETE "/{id}"         204; 404
  Register in main.py next to the others (one include_router line).

MIGRATION
Hand-write a reversible Alembic migration (autogenerate is unreliable). Create the
field_notes table matching bedf3037f156_create_initial_schema.py style: all
columns above, media as JSONB, the three check constraints, and a unique index on
slug. No enum type is created (status is String(20) + check constraint). Downgrade
drops the table.

STATUS CODES  201 create, 204 delete, 404 not found, 409 slug conflict, 422 FK /
invalid reference. Path kebab-case (/field-notes); slug values snake_case.

ACCEPTANCE (paste results into the PR)
- App boots (lifespan SELECT 1 passes).
- alembic upgrade head applies; downgrade drops the table cleanly.
- /docs lists all six Field Notes routes.
- curl:
    a. create a visual-only draft (poem + media, NO essay) -> 201, media returns intact
    b. create a full draft (poem + media + essay + excerpt) -> 201
    c. GET by id and GET via list
    d. PATCH the title and replace media -> media updated
    e. POST /publish -> status published, published_at set
    f. re-POST /publish -> 200, published_at unchanged
    g. create a second note with a duplicate slug -> 409
    h. create with empty poem "" -> rejected (422)
    i. confirm POST and PATCH cannot set status (no such field accepted)
- psql: SELECT id, slug, status, published_at FROM field_notes;

BRANCH / PR
- Branch: feature/field-notes-api. Diff limited to the new resource files, the two
  enum additions in app/enums.py, and one include_router line in main.py.
- PR title: "Field Notes resource (visual essay CRUD)".
-->


## GOAL
Amend the existing Field Notes resource: add an optional "sources" field for
external references (the reader-facing citations under part two). It mirrors the
existing "media" field exactly, at every layer. No provenance, no associations, no
uploads, no frontend, no other resource touched.

READ FIRST, THEN MIRROR MEDIA
- The current Field Notes files as just built:
  app/models/field_note.py, app/schemas/field_note.py,
  app/services/field_note.py (create + update media handling),
  app/routers/field_note.py
- app/enums.py (MediaKind, for the enum style to copy)
- The field_notes migration alembic/versions/8c2d4e5f6a7b_*.py (current head) for
  column + style, and to chain from it
Wherever "media" appears, "sources" gets the parallel treatment. Do not change any
media behavior.

ENUM  app/enums.py  (UPPER name / lower value, same as MediaKind)
  class SourceKind(StrEnum):
      ARTICLE = "article"
      REPO = "repo"
      DOC = "doc"
      TOOL = "tool"
      BOOK = "book"
Validation only (lives inside the JSONB payload, like MediaKind). No DB constraint.

MODEL  app/models/field_note.py
Add one column, mirroring media (JSONB, nullable), positioned right after essay:
  sources: Mapped[list[dict] | None] = mapped_column(JSONB)

SCHEMA  app/schemas/field_note.py
- Add, mirroring MediaRef:
    class SourceRef(BaseModel):
        label: str = Field(min_length=1)
        url: str | None = None
        kind: SourceKind | None = None
- Add to FieldNoteBase (so it appears on Create and Read):
    sources: list[SourceRef] | None = None
- Add the identical optional field to FieldNoteUpdate.
- Keep the existing extra="forbid" config on the request schemas unchanged.
- FieldNoteRead needs no extra work; it inherits sources from Base.

SERVICE  app/services/field_note.py
- create_field_note: add explicit assignment mirroring media:
    sources=[s.model_dump() for s in payload.sources] if payload.sources else None
- update_field_note: the model_dump(exclude_unset=True) setattr loop already
  serializes nested SourceRef lists to list[dict], same as media. Confirm sources
  round-trips through PATCH; add nothing special unless it does not.

MIGRATION
One reversible Alembic revision chained from head 8c2d4e5f6a7b:
- upgrade: op.add_column("field_notes", sa.Column("sources", JSONB(), nullable=True))
- downgrade: op.drop_column("field_notes", "sources")

STATUS CODES  unchanged. Invalid source kind -> 422 (Pydantic). Extra top-level
field on a note -> 422 (existing extra=forbid).

ACCEPTANCE (paste into as output and into the PR)
- seed file scripts/seed_field_notes.py runs clean against the amended schema. Running it creates and publishes the note with sources persisted and returned. 
- App boots; alembic upgrade head then downgrade -1 add and drop the column cleanly.
- /docs shows sources (list of SourceRef) on Create, Update, Read.
- curl:
    a. create a note with sources=[{"label":"...", "url":"...", "kind":"repo"}] -> 201, sources returned intact
    b. create a note with no sources -> 201, sources is null
    c. PATCH replaces sources -> updated
    d. create with sources kind "podcast" (not in enum) -> 422
    e. media behavior unchanged (a media create still works)
- psql: SELECT id, slug, sources FROM field_notes;

BRANCH / PR
- If feature/field-notes-api is not yet merged, add this to it.
- If it is merged, branch feature/field-notes-sources off main.
- Diff limited to: one enum, the sources column, the SourceRef schema + two field
  additions, the create-service line, and one migration.
- PR title: "Field Notes: sources (external references)".
