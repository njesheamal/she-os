from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constraints import status_in
from app.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.enums import ItemStatus


class Item(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    sku: Mapped[str | None] = mapped_column(String(100), unique=True)
    item_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("item_types.id"), nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    __table_args__ = (
        CheckConstraint("name <> ''", name="name_not_empty"),
        CheckConstraint("slug <> ''", name="slug_not_empty"),
        CheckConstraint("sku <> ''", name="sku_not_empty"),
        CheckConstraint(status_in(ItemStatus), name="status_valid"),
    )
