from __future__ import annotations
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings


@lru_cache(maxsize=1)
def get_engine():
    db_url = settings.db_url
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite///") or db_url.startswith("sqlite:///") else {}
    return create_engine(db_url, pool_pre_ping=True, future=True, connect_args=connect_args)


def get_sessionmaker():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, future=True)


# Backward compat exports
engine = get_engine()
SessionLocal = get_sessionmaker()


def get_db():
    db = get_sessionmaker()()
    try:
        yield db
    finally:
        db.close()
