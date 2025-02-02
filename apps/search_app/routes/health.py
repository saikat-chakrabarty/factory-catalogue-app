from fastapi import APIRouter
from libs.catalogue.db import engine
from sqlalchemy.exc import OperationalError

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    try:
        # A simple health check by executing a raw SQL
        with engine.connect() as connection:
            connection.execute("SELECT 1")
    except OperationalError:
        return {"status": "fail", "detail": "Database connection failed"}
    return {"status": "ok"}
