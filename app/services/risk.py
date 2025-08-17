from __future__ import annotations
from typing import Optional
from ..config import settings

BOT_UA_DENY = ["curl", "bot", "spider", "crawler"]

_velocity_cache: dict[tuple[str, int], int] = {}
_fp_seen: set[tuple[str, int]] = set()


def _bucket_10m(ts_minute: int) -> int:
    return (ts_minute // 10) * 10


def evaluate(ip: str, ua: str, referer: Optional[str], country: Optional[str], asn: Optional[str], link_id: int, partner_id: int, fingerprint: Optional[str]) -> tuple[float, bool]:
    ua_lower = (ua or "").lower()
    if any(b in ua_lower for b in BOT_UA_DENY):
        return 0.0, False

    if asn and asn in set(settings.ASN_DENYLIST):
        return 0.2, False

    if settings.COUNTRY_ALLOWLIST and (country or "").upper() not in set(settings.COUNTRY_ALLOWLIST):
        return 0.3, False

    # velocity per IP per 10m bucket (in-memory MVP)
    import time
    minute = int(time.time() // 60)
    bucket = _bucket_10m(minute)
    key = (ip or "?", bucket)
    _velocity_cache[key] = _velocity_cache.get(key, 0) + 1
    if _velocity_cache[key] > settings.RISK_VELOCITY_MAX_10M:
        return 0.4, False

    # Cookie/fingerprint dedupe per link_id for 24h (MVP in-memory without TTL)
    payable = True
    if fingerprint:
        fp_key = (fingerprint, link_id)
        if fp_key in _fp_seen:
            payable = False
        else:
            _fp_seen.add(fp_key)

    base = 0.75
    final_payable = payable and base >= 0.6
    return base, final_payable
