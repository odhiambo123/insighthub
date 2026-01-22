from fastapi import APIRouter, Depends
from app.api.deps.auth import get_current_user
from app.schemas.user import UserRead
from app.api.deps.rbac import require_role

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Welcome admin"}


@router.get("/me", response_model=UserRead)
def read_me(user=Depends(require_role("user", "admin"))):
    return user


@router.get("/profile", response_model=UserRead)
def profile(user=Depends(require_role("user", "admin"))):
    return user
