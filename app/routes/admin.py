from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db_dep, require_admin
from ..models import ClickEvent, Balance, Link

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/overview")
async def overview(_: bool = Depends(require_admin), db: Session = Depends(get_db_dep)):
    raw_clicks = db.query(ClickEvent).count()
    payable_clicks = db.query(ClickEvent).filter(ClickEvent.payable == True).count()
    total_earnings = float(db.query(Balance.lifetime_eur).first()[0] if db.query(Balance).count() else 0)
    partners = db.query(Balance).count()
    return {"raw_clicks": raw_clicks, "payable_clicks": payable_clicks, "total_earnings": total_earnings, "partners": partners}
