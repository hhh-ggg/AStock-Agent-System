from fastapi import APIRouter

from app.db.session import check_db_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/db")
def health_db():
    result = check_db_connection()
    return result
