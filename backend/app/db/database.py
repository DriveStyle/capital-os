from __future__ import annotations

from typing import Any

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ..config import get_settings


def get_database_url() -> str:
    return get_settings().database_url


engine: Engine | None = None
SessionLocal: sessionmaker[Any] | None = None


def initialize_database() -> None:
    global engine, SessionLocal
    if engine is None or SessionLocal is None:
        from sqlalchemy import create_engine
        url = get_database_url()
        connect_args = {}
        if url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
            engine = create_engine(url, connect_args=connect_args)
        else:
            engine = create_engine(url, pool_pre_ping=True)
            
        SessionLocal = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True,
        )


def get_engine() -> Engine:
    initialize_database()
    assert engine is not None
    return engine


def get_session_local() -> sessionmaker[Any]:
    initialize_database()
    assert SessionLocal is not None
    return SessionLocal
