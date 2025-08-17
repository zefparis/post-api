from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import jwt
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


class MagicLinkRequest(BaseModel):
    email: EmailStr


@router.post("/magic-link")
async def magic_link(req: MagicLinkRequest):
    # Dev mode: log link
    token = jwt.encode({"email": req.email, "scope": "partner"}, settings.JWT_SECRET, algorithm="HS256")
    link = f"{settings.APP_BASE_URL}/api/auth/verify?token={token}"
    print(f"[dev-magic-link] {link}")
    return {"ok": True}


class VerifyRequest(BaseModel):
    token: str


@router.post("/verify")
async def verify(req: VerifyRequest):
    try:
        payload = jwt.decode(req.token, settings.JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=400, detail="Token invalide")
    # Return JWT for partner scope
    jwt_out = jwt.encode({"sub": payload.get("email"), "scope": "partner"}, settings.JWT_SECRET, algorithm="HS256")
    return {"access_token": jwt_out, "token_type": "bearer"}
