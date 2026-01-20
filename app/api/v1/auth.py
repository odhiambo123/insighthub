from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps.db import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import get_user_by_email
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(user_in: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": create_refresh_token(str(user.id)),
        "token_type": "bearer",
    }
