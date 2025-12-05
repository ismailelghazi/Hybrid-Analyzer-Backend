from fastapi import FastAPI as fs
from app.routers.db_check import router as db_router  # import DB router
from app.routers.auth import router as auth_router

app = fs()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# DB test routes
app.include_router(db_router)
