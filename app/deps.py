from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .config import settings
from sqlalchemy.orm import Session
from .db import get_db

bearer = HTTPBearer(auto_error=False)


def get_current_partner(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non authentifié")
    try:
        payload = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Jeton invalide")
    if payload.get("scope") != "partner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Portée invalide")
    return payload


def require_admin(token: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not token or token.credentials != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Accès admin refusé")
    return True

get_db_dep = get_db
