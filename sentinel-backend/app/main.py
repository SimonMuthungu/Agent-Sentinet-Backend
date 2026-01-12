from fastapi import FastAPI
from app.api import vendors, evaluations, escalations, audit, dashboard, uploads
from app.api.health import router as health_router
from app.services.scheduler import start_scheduler
from app.api.debug import router as debug_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Sentinel Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(vendors.router, prefix="/vendors")
# app.include_router(evaluations.router, prefix="/evaluations")
app.include_router(escalations.router, prefix="/escalations")
app.include_router(audit.router, prefix="/audit")
app.include_router(debug_router)
app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(uploads.router, prefix="")


@app.get("/")
async def root():
    """
    Root endpoint for service verification.
    """
    return {"message": "Welcome to Sentinel Backend"}


# @app.on_event("startup")
async def startup():
    start_scheduler()
