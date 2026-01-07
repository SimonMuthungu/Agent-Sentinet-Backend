from fastapi import APIRouter
from app.agents.graph_runner import run_vendor_evaluation

router = APIRouter()

@router.post("/debug/run/{vendor_id}")
async def debug_run(vendor_id: str):
    return await run_vendor_evaluation(
        vendor_id=vendor_id,
        query="Test compliance evaluation"
    )
