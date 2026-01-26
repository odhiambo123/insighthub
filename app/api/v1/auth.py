from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import uuid

from app.api.deps.db import get_db
from app.services.user_service import get_user_by_email
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.models.refresh_token import RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token_value = str(uuid.uuid4())

    db_token = RefreshToken(
        token=refresh_token_value,
        user_id=user.id,
        revoked=False,
    )
    db.add(db_token)
    db.commit()

    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "refresh_token": refresh_token_value,
        "token_type": "bearer",
        "expires_in": 1800  # seconds (30 min)
    }


@router.post("/refresh")
def refresh_token(
    payload: RefreshTokenRequest,
    db=Depends(get_db),
):
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == payload.refresh_token,
            RefreshToken.revoked == False,
        )
        .first()
    )

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {
        "access_token": create_access_token({"sub": str(db_token.user_id)}),
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(
    payload: RefreshTokenRequest,
    db=Depends(get_db),
):
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == payload.refresh_token)
        .first()
    )

    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid token")

    db_token.revoked = True
    db.commit()

    return {"message": "Logged out successfully"}
