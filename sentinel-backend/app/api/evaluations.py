from fastapi import APIRouter
from app.domain.schemas import EvaluationRequest
from app.agents.graph import vendor_graph

router = APIRouter()

@router.post("/")
async def evaluate_vendor(req: EvaluationRequest):
    result = await vendor_graph.ainvoke({
        "vendor_id": req.vendor_id,
        "vendor_name": "Unknown Vendor",
        "retrieved_docs": [],
        "final_assessment": ""
    })

    return result
