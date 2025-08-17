from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db_dep, get_current_partner
from ..models import ClickEvent, Balance, Link

router = APIRouter(prefix="/api/partner", tags=["partner"])


@router.get("/stats/summary")
async def stats_summary(payload = Depends(get_current_partner), db: Session = Depends(get_db_dep)):
    sub = payload.get("sub") or payload.get("email")
    # MVP: aggregate for all partners (or could filter by sub if mapping exists)
    raw_clicks = db.query(ClickEvent).count()
    payable_clicks = db.query(ClickEvent).filter(ClickEvent.payable == True).count()
    earnings = float(db.query(Balance.lifetime_eur).first()[0] if db.query(Balance).count() else 0)
    epc = earnings / payable_clicks if payable_clicks else 0
    links_count = db.query(Link).count()
    return {"raw_clicks": raw_clicks, "payable_clicks": payable_clicks, "earnings": earnings, "epc": epc, "links": links_count}
