from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_users
from app.api.deps.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


# ✅ PUBLIC: Create user (signup)
@router.post("/", response_model=UserRead)
def create_user_endpoint(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user_in)


# 🔒 PROTECTED: List users
@router.get("/", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_users(db)
