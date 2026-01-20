from fastapi import APIRouter, Depends
from app.api.deps.rbac import require_role
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile")
def profile(user=Depends(require_role("user", "admin"))):
    return user
