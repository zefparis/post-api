from __future__ import annotations
from sqlalchemy.orm import Session
from ..models import MetricEvent


def record(db: Session, *, kind: str, value: float, post_id: int | None = None, platform: str | None = None, metadata_json: str | None = None) -> MetricEvent:
    ev = MetricEvent(kind=kind, value=value, post_id=post_id, platform=platform, metadata_json=metadata_json)
    db.add(ev)
    try:
        db.flush()
    except Exception:
        db.rollback()
        raise
    return ev
