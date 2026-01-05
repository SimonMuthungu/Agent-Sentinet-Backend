from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Simple health check endpoint to verify service status.
    """
    return {"status": "ok", "service": "Sentinel Backend"}
