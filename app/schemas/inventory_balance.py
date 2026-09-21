from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InventoryBalanceRead(BaseModel):
    """Current tracked quantity for an item at a location."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    item_id: UUID
    inventory_location_id: UUID
    quantity_on_hand: Decimal
    unit_of_measure_id: UUID
    created_at: datetime
    updated_at: datetime
