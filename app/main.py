from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router

app = FastAPI(title="InsightHub")

app.include_router(health_router)
app.include_router(users_router, prefix="/api/v1")
