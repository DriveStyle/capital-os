from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session

from .database import get_session_local


def get_db() -> Iterator[Session]:
    session_factory = get_session_local()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
