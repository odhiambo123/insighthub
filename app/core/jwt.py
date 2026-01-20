from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings


def create_access_token(sub: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub": sub,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(sub: str):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        "sub": sub,
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
