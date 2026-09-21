from sqlalchemy import Boolean, CheckConstraint, String, Text, text
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class LookupBase(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true"), index=True
    )

    @declared_attr.directive
    def __table_args__(cls):
        return (
            CheckConstraint("name <> ''", name="name_not_empty"),
            CheckConstraint("slug <> ''", name="slug_not_empty"),
        )


class ItemType(LookupBase):
    __tablename__ = "item_types"


class PartnerType(LookupBase):
    __tablename__ = "partner_types"


class InitiativeType(LookupBase):
    __tablename__ = "initiative_types"


class InventoryLocationType(LookupBase):
    __tablename__ = "inventory_location_types"


class InventoryMovementType(LookupBase):
    __tablename__ = "inventory_movement_types"


class UnitOfMeasure(LookupBase):
    __tablename__ = "units_of_measure"
