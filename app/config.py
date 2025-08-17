from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json
from typing import List
import os
import re


_DB_POSTGRES_RE = re.compile(r"^postgres(ql)?(\+[\w]+)?://", re.I)


def _normalize_db_url(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return "sqlite:///./local.db"
    # strip accidental quotes
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1].strip()
    # postgres -> postgresql(+psycopg2)
    m = _DB_POSTGRES_RE.match(v)
    if m:
        has_ql = bool(m.group(1))
        has_driver = bool(m.group(2))
        if not has_ql:
            v = v.replace("postgres://", "postgresql://", 1)
        if not has_driver:
            v = v.replace("postgresql://", "postgresql+psycopg2://", 1)
    # sqlite ensure triple slash
    if v.startswith("sqlite://") and ":///" not in v:
        v = v.replace("sqlite://", "sqlite:///", 1)
    return v


def _parse_list(value: str | list | None) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    v = value.strip()
    try:
        if v.startswith("[") or v.startswith("{"):
            parsed = json.loads(v)
            return parsed if isinstance(parsed, list) else []
    except Exception:
        pass
    # CSV
    return [x.strip() for x in v.split(",") if x.strip()]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    DATABASE_URL: str = "sqlite:///./local.db"
    JWT_SECRET: str = "changeme"
    APP_BASE_URL: str = "http://localhost:8000"
    PUBLIC_BASE_URL: str = "http://localhost:8000"

    CPC_DEFAULT_EUR: float = 0.11
    CPC_MIN_EUR: float = 0.06
    CPC_MAX_EUR: float = 0.20

    RISK_VELOCITY_MAX_10M: int = 40
    ASN_DENYLIST: List[str] = []
    COUNTRY_ALLOWLIST: List[str] = ["FR", "BE", "CA"]

    HOLD_DAYS: int = 30
    RESERVE_PCT: float = 0.30

    ADMIN_TOKEN: str = "changeme-admin"

    PORT: int = 8000

    @field_validator("ASN_DENYLIST", "COUNTRY_ALLOWLIST", mode="before")
    @classmethod
    def parse_list(cls, v):
        return _parse_list(v)

    @field_validator("APP_BASE_URL", mode="before")
    @classmethod
    def prefer_railway_app(cls, v):
        domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if domain and (v is None or "localhost" in str(v)):
            return f"https://{domain}"
        return v

    @field_validator("PUBLIC_BASE_URL", mode="before")
    @classmethod
    def prefer_railway_public(cls, v):
        domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if domain and (v is None or "localhost" in str(v)):
            return f"https://{domain}"
        return v

    @property
    def db_url(self) -> str:
        env_v = os.getenv("DATABASE_URL", self.DATABASE_URL)
        return _normalize_db_url(env_v)


settings = Settings()
