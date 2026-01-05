from fastapi import FastAPI
from app.config import settings
from app.api import health, vendors, evaluations, escalations

app = FastAPI(title=settings.app_name)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(vendors.router, prefix="/api/v1/vendors", tags=["Vendors"])
app.include_router(evaluations.router, prefix="/api/v1/evaluations", tags=["Evaluations"])
app.include_router(escalations.router, prefix="/api/v1/escalations", tags=["Escalations"])

@app.get("/")
async def root():
    """
    Root endpoint for service verification.
    """
    return {"message": "Welcome to Sentinel Backend"}
