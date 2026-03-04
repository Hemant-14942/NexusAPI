"""Health check endpoint."""
from datetime import datetime, timezone
from fastapi import APIRouter, status,Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
import uuid

from app.database import AsyncSessionLocal
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """
    GET /health — returns application status and confirms the database is reachable.
    Returns HTTP 503 if the database is unreachable.
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "healthy",
                "database": "reachable",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        # Grab the request_id from the middleware, fallback to a new UUID just in case
        request_id = str(getattr(request.state, "request_id", uuid.uuid4()))

        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "error": "database_unreachable",
                    "message": "The database is temporarily unreachable.",
                    "request_id": request_id,
                },
            )
