from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

DB_URL = settings.db_url

connect_args = {}
if DB_URL.startswith("sqlite///") or DB_URL.startswith("sqlite:///"):
    # SQLite needs this when used with FastAPI threads
    connect_args = {"check_same_thread": False}

engine = create_engine(DB_URL, pool_pre_ping=True, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
