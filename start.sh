#!/usr/bin/env sh
set -e
PORT_RESOLVED="${PORT:-8000}"
echo "[boot] Using PORT=${PORT_RESOLVED}"
DB_SHOW="${DATABASE_URL:-unset}"
# mask credentials if present
case "$DB_SHOW" in
  *://*:*@*)
    SCHEME=$(printf "%s" "$DB_SHOW" | sed -E 's#^([^:]+)://.*$#\1#')
    HOSTPART=$(printf "%s" "$DB_SHOW" | sed -E 's#^[^/]+://[^@]+@(.*)$#\1#')
    DB_SHOW="${SCHEME}://***@${HOSTPART}"
    ;;
esac
echo "[boot] DB=${DB_SHOW}"
if [ "${DISABLE_ALEMBIC:-0}" = "1" ]; then
  echo "[boot] DISABLE_ALEMBIC=1 → skipping migrations"
else
  if command -v alembic >/dev/null 2>&1; then
    echo "[boot] running alembic upgrade"
    if ! alembic upgrade head; then
      echo "[boot] alembic upgrade failed → stamping head"
      alembic stamp head || true
    fi
  else
    echo "[boot] alembic not found, skipping migrations"
  fi
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT_RESOLVED}" --log-level info --proxy-headers --forwarded-allow-ips="*"
