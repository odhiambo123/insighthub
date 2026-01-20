from fastapi import APIRouter, Depends
from app.api.deps.rbac import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": "Welcome admin"}
