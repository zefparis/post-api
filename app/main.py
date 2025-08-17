# app/main.py
from __future__ import annotations
import os
import logging
import mimetypes
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from .db import engine
from .models import Base
from .config import settings
from .routes import auth as auth_routes
from .routes import links as links_routes
from .routes import partner as partner_routes
from .routes import admin as admin_routes
from .routes import posts as posts_routes

# ---------- logging ----------
logger = logging.getLogger("contentflow")
logging.basicConfig(
    level=logging.INFO,
    format='{"level":"%(levelname)s","msg":"%(message)s"}'
)

# ---------- lifespans ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ready = False
    # SQLite/dev: create_all; en prod -> Alembic
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        logger.exception("DB init failure")
    # (NE RIEN AJOUTER qui fait app.add_middleware ici)
    app.state.ready = True
    yield
    # shutdown hooks si besoin ...

# ---------- app ----------
app = FastAPI(lifespan=lifespan)

# ---------- log DB url (masked) ----------
safe = settings.db_url
try:
    if "://" in safe:
        scheme, rest = safe.split("://", 1)
        if "@" in rest and ":" in rest.split("@", 1)[0]:
            user = rest.split("@", 1)[0].split(":", 1)[0]
            hostpart = rest.split("@", 1)[1]
            safe = f"{scheme}://{user}:***@{hostpart}"
except Exception:
    pass
logger.info(f"[db] Using {safe}")

# ---------- prometheus (AVANT démarrage) ----------
try:
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers={"/metrics"},
    ).instrument(app).expose(app)
    logger.info("Prometheus metrics exposé sur /metrics")
except Exception as e:
    logger.warning(f"Prometheus init skipped: {e}")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "CORS_ORIGINS", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- helpers ----------
# certains environnements slim ratent le mime type
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")

EXCLUDE_PREFIXES = (
    "/api", "/docs", "/redoc", "/openapi.json",
    "/static", "/assets", "/health", "/healthz", "/readyz", "/__feature_flags",
)

class LegacyRewriteMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # hook pour réécritures si besoin
        # ex:
        # if request.url.path.startswith("/partners/api/"):
        #     request.scope["path"] = request.url.path.replace("/partners/api", "/api", 1)
        return await call_next(request)

class SPAFallbackMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.static_root = Path(__file__).with_name("static")

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDE_PREFIXES):
            return await call_next(request)

        # servir fichier direct si présent
        if self.static_root.exists():
            file_path = (self.static_root / path.lstrip("/"))
            if file_path.is_file():
                return FileResponse(str(file_path))

        # laisser l'app répondre; si 404 on fera fallback index.html
        resp = await call_next(request)
        if getattr(resp, "status_code", None) != 404:
            return resp

        # fallback index.html
        index_html = self.static_root / "index.html"
        if index_html.exists():
            return FileResponse(str(index_html))
        return resp

# ordre: rewrite -> spa fallback
app.add_middleware(LegacyRewriteMiddleware)
app.add_middleware(SPAFallbackMiddleware)

# ---------- health ----------
@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}

@app.get("/readyz", include_in_schema=False)
def readyz():
    ready = bool(getattr(app.state, "ready", False))
    return JSONResponse({"ready": ready}, status_code=200 if ready else 503)

# ---------- routers ----------
app.include_router(auth_routes.router)
app.include_router(posts_routes.router)
app.include_router(links_routes.router)
app.include_router(partner_routes.router)
app.include_router(admin_routes.router)

# ---------- static (build Vite copié en app/static) ----------
static_dir = Path(__file__).with_name("static")
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
