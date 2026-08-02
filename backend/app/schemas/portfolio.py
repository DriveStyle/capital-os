from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    owner_id: UUID


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PortfolioResponse(PortfolioBase):
    id: UUID
    owner_id: UUID
    total_value: Optional[Decimal] = Decimal("0.00")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
