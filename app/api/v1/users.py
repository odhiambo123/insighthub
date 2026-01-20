from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.api.deps.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.services.user_service import get_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_users(db)
