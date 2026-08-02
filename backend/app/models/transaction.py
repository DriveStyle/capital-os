from __future__ import annotations

import uuid
from datetime import datetime

from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base
from ..db.types import GUID


class Transaction(Base):
    __tablename__ = "transactions"

    id = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    transaction_type = mapped_column(String(50), nullable=False)
    amount = mapped_column(Numeric(12, 2), nullable=False)
    currency = mapped_column(String(10), default="USD", nullable=False)
    description = mapped_column(Text, nullable=True)
    executed_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    portfolio_id = mapped_column(
        GUID,
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="transactions")
