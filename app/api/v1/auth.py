from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.db import get_db
from app.services.user_service import get_user_by_email
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from jose import jwt, JWTError
from app.core.config import settings
from app.services.user_service import get_user_by_id

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": create_access_token(data={"sub": str(user.id)}),
        "refresh_token": create_refresh_token(data={"sub": str(user.id)}),
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(refresh_token: str, db=Depends(get_db)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=401, detail="Invalid token subject")

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "access_token": create_access_token(
                data={"sub": str(user.id)}
            ),
            "token_type": "bearer",
        }

    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid or expired refresh token"
        )
