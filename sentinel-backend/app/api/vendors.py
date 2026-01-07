from fastapi import APIRouter
from app.agents.graph_runner import run_vendor_evaluation

router = APIRouter()

@router.post("/{vendor_id}/evaluate")
async def evaluate_vendor(vendor_id: str, query: str):
    return await run_vendor_evaluation(vendor_id, query)
