from __future__ import annotations
from sqlalchemy.orm import Session
from ..config import settings
from ..models import ClickEvent, Balance
from ..utils.datetime import utcnow


def clamp_amount(eur: float) -> float:
    return max(settings.CPC_MIN_EUR, min(settings.CPC_MAX_EUR, eur))


def apply_click(db: Session, *, link_id: int, partner_id: int, risk_score: float, payable: bool) -> ClickEvent:
    amount = clamp_amount(settings.CPC_DEFAULT_EUR) if payable else 0.0
    ev = ClickEvent(
        link_id=link_id,
        partner_id=partner_id,
        ip="", ua="", referer=None, country=None, asn=None, fingerprint=None,
        risk_score=risk_score,
        payable_amount_eur=amount,
        payable=payable,
    )
    db.add(ev)
    # ensure balance row
    bal = db.query(Balance).filter(Balance.partner_id == partner_id).one_or_none()
    if not bal:
        bal = Balance(partner_id=partner_id, available_eur=0, on_hold_eur=0, lifetime_eur=0)
        db.add(bal)
    if payable:
        bal.on_hold_eur = (bal.on_hold_eur or 0) + amount
        bal.lifetime_eur = (bal.lifetime_eur or 0) + amount
        bal.updated_at = utcnow()
    db.flush()
    return ev
