from jose import JWTError, jwt
from app.core.jwt import create_access_token
from app.core.config import settings
from fastapi import APIRouter

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
    }
