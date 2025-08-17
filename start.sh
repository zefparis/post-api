#!/usr/bin/env sh
set -e
PORT_RESOLVED="${PORT:-8000}"
echo "[boot] Using PORT=${PORT_RESOLVED}"
if command -v alembic >/dev/null 2>&1; then
  echo "[boot] Running Alembic migrations"
  alembic upgrade head || echo "[boot] Alembic failed (continuing for dev)"
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT_RESOLVED}" --log-level info --proxy-headers --forwarded-allow-ips="*"
