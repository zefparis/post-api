from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..deps import get_db_dep, get_current_partner
from ..models import Link, Post
from ..services import risk as risk_svc, ledger as ledger_svc
from ..config import settings
import secrets
import string

router = APIRouter(tags=["links"])


class CreateLinkRequest(BaseModel):
    post_id: int


def _gen_code(n: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(n))


@router.post("/api/links")
async def create_link(payload = Depends(get_current_partner), req: CreateLinkRequest = None, db: Session = Depends(get_db_dep)):
    post = db.query(Post).filter(Post.id == req.post_id).one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post introuvable")
    code = _gen_code()
    link = Link(code=code, post_id=post.id, partner_id=post.partner_id)
    db.add(link)
    db.flush()
    return {"code": code, "url": f"{settings.PUBLIC_BASE_URL}/r/{code}"}


@router.get("/r/{code}")
async def redirect(code: str, request: Request, response: Response, db: Session = Depends(get_db_dep)):
    link = db.query(Link).filter(Link.code == code).one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    post = db.query(Post).filter(Post.id == link.post_id).one()

    ip = request.client.host if request.client else "?"
    ua = request.headers.get("user-agent", "?")
    referer = request.headers.get("referer")
    country = request.headers.get("cf-ipcountry")
    asn = request.headers.get("cf-asn")
    fingerprint = request.cookies.get("cf_fp")

    risk_score, payable = risk_svc.evaluate(ip, ua, referer, country, asn, link.id, link.partner_id, fingerprint)

    # set cookie once per 24h for dedupe (MVP simplified)
    response.set_cookie("cf_fp", fingerprint or secrets.token_hex(8), max_age=60*60*24, httponly=False, samesite="Lax")

    ev = ledger_svc.apply_click(db, link_id=link.id, partner_id=link.partner_id, risk_score=risk_score, payable=payable)
    db.commit()

    response.status_code = 302
    response.headers["Location"] = post.target_url
    return response
