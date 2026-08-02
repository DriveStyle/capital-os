from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    transaction_type: str  # e.g., 'buy', 'sell', 'deposit', 'withdrawal'
    amount: Decimal
    currency: str = "USD"
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    portfolio_id: UUID


class TransactionResponse(TransactionBase):
    id: UUID
    portfolio_id: UUID
    executed_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
