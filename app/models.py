from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, Boolean
from datetime import datetime, timezone


def tznow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Partner(Base):
    __tablename__ = "partners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)
    api_key_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)
    payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    title: Mapped[str] = mapped_column(String(255))
    target_url: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)
    status: Mapped[str] = mapped_column(String(50), default="active")


class Link(Base):
    __tablename__ = "links"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)


class ClickEvent(Base):
    __tablename__ = "click_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"), index=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow, index=True)
    ip: Mapped[str] = mapped_column(String(64))
    ua: Mapped[str] = mapped_column(String(512))
    referer: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    country: Mapped[str | None] = mapped_column(String(8), nullable=True)
    asn: Mapped[str | None] = mapped_column(String(16), nullable=True)
    fingerprint: Mapped[str | None] = mapped_column(String(128), nullable=True)
    risk_score: Mapped[float] = mapped_column(Float)
    payable_amount_eur: Mapped[float] = mapped_column(Float, default=0)
    payable: Mapped[bool] = mapped_column(Boolean, default=False)


class MetricEvent(Base):
    __tablename__ = "metric_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), nullable=True)
    platform: Mapped[str | None] = mapped_column(String(64), nullable=True)
    kind: Mapped[str] = mapped_column(String(64))
    value: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class Balance(Base):
    __tablename__ = "balances"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"), unique=True)
    available_eur: Mapped[float] = mapped_column(Float, default=0)
    on_hold_eur: Mapped[float] = mapped_column(Float, default=0)
    lifetime_eur: Mapped[float] = mapped_column(Float, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(64))
    payload: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tznow)
