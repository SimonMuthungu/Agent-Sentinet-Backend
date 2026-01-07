from fastapi import FastAPI
from app.api import vendors, evaluations, escalations
from app.api.health import router as health_router
from app.services.scheduler import start_scheduler
from app.api.debug import router as debug_router


app = FastAPI(title="Sentinel Backend")

app.include_router(health_router)
app.include_router(vendors.router, prefix="/vendors")
app.include_router(evaluations.router, prefix="/evaluations")
app.include_router(escalations.router, prefix="/escalations")
app.include_router(debug_router)


@app.get("/")
async def root():
    """
    Root endpoint for service verification.
    """
    return {"message": "Welcome to Sentinel Backend"}


# @app.on_event("startup")
async def startup():
    start_scheduler()
