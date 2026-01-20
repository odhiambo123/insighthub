from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import get_user_by_email
from app.core.security import verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user_in: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}
