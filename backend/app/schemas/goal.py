from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_amount: Decimal
    target_date: Optional[datetime] = None


class GoalCreate(GoalBase):
    user_id: UUID


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[Decimal] = None
    target_date: Optional[datetime] = None


class GoalResponse(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
