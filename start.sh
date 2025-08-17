#!/usr/bin/env sh
set -e
PORT_RESOLVED="${PORT:-8000}"
echo "[boot] Using PORT=${PORT_RESOLVED}"
echo "[boot] DB=${DATABASE_URL:-unset}"
if command -v alembic >/dev/null 2>&1; then
  echo "[boot] running alembic upgrade"
  if ! alembic upgrade head; then
    echo "[boot] alembic upgrade failed → stamping head"
    alembic stamp head || true
  fi
else
  echo "[boot] alembic not found, skipping migrations"
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT_RESOLVED}" --log-level info --proxy-headers --forwarded-allow-ips="*"
