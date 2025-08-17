from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, AnyHttpUrl
from sqlalchemy.orm import Session
from ..deps import get_db_dep, get_current_partner
from ..models import Asset, Post
from ..services.ai import generate_asset

router = APIRouter(tags=["posts"]) 


class CreatePostRequest(BaseModel):
    title_hint: str | None = None
    target_url: AnyHttpUrl


@router.post("/api/posts")
async def create_post(payload = Depends(get_current_partner), req: CreatePostRequest = None, db: Session = Depends(get_db_dep)):
    a = generate_asset(req.title_hint)
    asset = Asset(title=a["title"], summary=a["summary"], payload_json=str(a["payload"]), partner_id=1)
    db.add(asset)
    db.flush()
    post = Post(asset_id=asset.id, partner_id=1, title=asset.title, target_url=str(req.target_url))
    db.add(post)
    db.flush()
    return {"post_id": post.id}
