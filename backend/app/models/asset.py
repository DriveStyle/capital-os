from __future__ import annotations

import uuid
from datetime import datetime

from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    symbol = mapped_column(String(50), nullable=False, index=True)
    asset_type = mapped_column(String(50), nullable=False)
    quantity = mapped_column(Numeric(12, 6), nullable=True)
    cost_basis = mapped_column(Numeric(12, 2), nullable=True)
    current_value = mapped_column(Numeric(12, 2), nullable=True)
    notes = mapped_column(Text, nullable=True)
    portfolio_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="assets")
