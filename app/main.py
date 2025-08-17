from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import FileResponse
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
import os


logger = logging.getLogger("contentflow")
logging.basicConfig(level=logging.INFO, format='{"level":"%(levelname)s","msg":"%(message)s"}')


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ready = False
    # Ensure tables exist for SQLite dev; in prod use Alembic migrations
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        logger.exception("DB init failure")
    Instrumentator().instrument(app).expose(app)
    app.state.ready = True
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LegacyRewriteMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await call_next(request)


EXCLUDE_PREFIXES = (
    "/api", "/docs", "/redoc", "/openapi.json", "/static", "/assets", "/healthz", "/readyz", "/__feature_flags",
)


class SPAFallbackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDE_PREFIXES):
            return await call_next(request)
        # try file
        static_root = os.path.join(os.path.dirname(__file__), "static")
        file_path = os.path.join(static_root, path.lstrip("/"))
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        index_html = os.path.join(static_root, "index.html")
        if os.path.isfile(index_html):
            return FileResponse(index_html)
        return await call_next(request)


app.add_middleware(LegacyRewriteMiddleware)
app.add_middleware(SPAFallbackMiddleware)


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/readyz")
def readyz():
    return ({"ready": True} if getattr(app.state, "ready", False) else Response(status_code=503))


# Routers
app.include_router(auth_routes.router)
app.include_router(posts_routes.router)
app.include_router(links_routes.router)
app.include_router(partner_routes.router)
app.include_router(admin_routes.router)

# Static mount (built app under app/static)
app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static"), html=True), name="static")
