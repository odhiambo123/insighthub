from fastapi import APIRouter, Depends
from app.api.deps.auth import get_current_user
from app.api.deps.rbac import require_role
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user
from app.api.deps.db import get_db

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


# @router.post("/", response_model=UserRead)
# def create_user_endpoint(
#    user_in: UserCreate,
#    db=Depends(get_db),
# ):
#    return create_user(db, user_in)

# for later
# @router.post("/", dependencies=[Depends(require_role("admin"))])
# so that only aadmins can add people

@router.post(
    "/",
    response_model=UserRead,
    dependencies=[Depends(require_role("admin"))]
)
def create_user_endpoint(
    user_in: UserCreate,
    db=Depends(get_db),
):
    return create_user(db, user_in)
