"""seed lookup values

Revision ID: 44f1b3c7682e
Revises: bedf3037f156
Create Date: 2026-08-16 06:54:26.521729

"""
from typing import Sequence, Union
from uuid import UUID

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44f1b3c7682e'
down_revision: Union[str, Sequence[str], None] = 'bedf3037f156'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Fixed UUIDs — identical across all environments. Do not regenerate.
SEED = {
    "item_types": [
        ("11111111-0000-4000-8000-000000000001", "material"),
        ("11111111-0000-4000-8000-000000000002", "component"),
        ("11111111-0000-4000-8000-000000000003", "sample"),
        ("11111111-0000-4000-8000-000000000004", "finished_product"),
        ("11111111-0000-4000-8000-000000000005", "packaging"),
        ("11111111-0000-4000-8000-000000000006", "asset"),
    ],
    "partner_types": [
        ("22222222-0000-4000-8000-000000000001", "supplier"),
        ("22222222-0000-4000-8000-000000000002", "manufacturer"),
        ("22222222-0000-4000-8000-000000000003", "crafter"),
        ("22222222-0000-4000-8000-000000000004", "tailor"),
        ("22222222-0000-4000-8000-000000000005", "pattern_maker"),
        ("22222222-0000-4000-8000-000000000006", "technical_designer"),
        ("22222222-0000-4000-8000-000000000007", "logistics_provider"),
    ],
    "initiative_types": [
        ("33333333-0000-4000-8000-000000000001", "collection"),
        ("33333333-0000-4000-8000-000000000002", "research"),
        ("33333333-0000-4000-8000-000000000003", "social_impact_program"),
    ],
    "inventory_location_types": [
        ("44444444-0000-4000-8000-000000000001", "warehouse"),
        ("44444444-0000-4000-8000-000000000002", "studio"),
        ("44444444-0000-4000-8000-000000000003", "production_site"),
        ("44444444-0000-4000-8000-000000000004", "event"),
        ("44444444-0000-4000-8000-000000000005", "temporary_storage"),
    ],
    "inventory_movement_types": [
        ("55555555-0000-4000-8000-000000000001", "receipt"),
        ("55555555-0000-4000-8000-000000000002", "transfer_in"),
        ("55555555-0000-4000-8000-000000000003", "transfer_out"),
        ("55555555-0000-4000-8000-000000000004", "adjustment_in"),
        ("55555555-0000-4000-8000-000000000005", "adjustment_out"),
        ("55555555-0000-4000-8000-000000000006", "damage"),
        ("55555555-0000-4000-8000-000000000007", "loss"),
        ("55555555-0000-4000-8000-000000000008", "consumption"),
        ("55555555-0000-4000-8000-000000000009", "sample"),
        ("55555555-0000-4000-8000-000000000010", "return_to_stock"),
    ],
    "units_of_measure": [
        ("66666666-0000-4000-8000-000000000001", "piece"),
        ("66666666-0000-4000-8000-000000000002", "bundle"),
        ("66666666-0000-4000-8000-000000000003", "set"),
        ("66666666-0000-4000-8000-000000000004", "pair"),
        ("66666666-0000-4000-8000-000000000005", "yard"),
        ("66666666-0000-4000-8000-000000000006", "meter"),
        ("66666666-0000-4000-8000-000000000007", "centimeter"),
        ("66666666-0000-4000-8000-000000000008", "kilogram"),
        ("66666666-0000-4000-8000-000000000009", "gram"),
        ("66666666-0000-4000-8000-000000000010", "liter"),
        ("66666666-0000-4000-8000-000000000011", "milliliter"),
        ("66666666-0000-4000-8000-000000000012", "roll"),
        ("66666666-0000-4000-8000-000000000013", "spool"),
        ("66666666-0000-4000-8000-000000000014", "box"),
        ("66666666-0000-4000-8000-000000000015", "carton"),
    ],
}


def _table(name: str) -> sa.Table:
    """Minimal ad-hoc table definition for insert/delete.

    Only the columns we touch. is_active and the timestamps have
    server defaults, so Postgres fills them; we omit them here.
    """
    # A migration should describe the database as it is at the time of the migration, not as it will be after the migration, using only what is stable. Migrations use lowercase sa.Table()/column() to avoid issues with case sensitivity and quoting. See https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.quote, while models use uppercase sa.Column() to match the model definition.
    return sa.table(
        name,
        sa.column("id", sa.Uuid),
        sa.column("name", sa.String),
        sa.column("slug", sa.String),
    )


def upgrade() -> None:
    for table_name, rows in SEED.items():
        op.bulk_insert(
            _table(table_name),
            [
                {"id": UUID(uuid_str), "name": value, "slug": value}
                for uuid_str, value in rows
            ],
        )


def downgrade() -> None:
    for table_name, rows in SEED.items():
        ids = [UUID(uuid_str) for uuid_str, _ in rows]
        tbl = _table(table_name)
        op.execute(tbl.delete().where(tbl.c.id.in_(ids)))