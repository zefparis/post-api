from datetime import datetime, timezone

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def iso_utc(dt: datetime | None = None) -> str:
    return (dt or utcnow()).isoformat()
