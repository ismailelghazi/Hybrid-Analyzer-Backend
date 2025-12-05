from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.database.connection import engine

router = APIRouter(
    prefix="/db",
    tags=["Database"]
)

@router.get("/test")
def test_db_connection():
    """
    Endpoint to check PostgreSQL connection.
    Returns OK if connected.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return {"db_status": "Connected to PostgreSQL!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f" DB connection failed: {e}")
    raise HTTPException(status_code=500, detail=" DB connection failed for unknown reasons.")