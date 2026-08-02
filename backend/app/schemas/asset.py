from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    symbol: str
    asset_type: str  # e.g., 'stock', 'etf', 'crypto', 'bond', 'cash'
    quantity: Decimal
    cost_basis: Decimal
    current_value: Decimal
    notes: Optional[str] = None


class AssetCreate(AssetBase):
    portfolio_id: UUID


class AssetUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    cost_basis: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    notes: Optional[str] = None


class AssetResponse(AssetBase):
    id: UUID
    portfolio_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
