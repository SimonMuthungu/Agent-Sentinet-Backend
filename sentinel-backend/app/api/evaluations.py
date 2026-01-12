# from fastapi import APIRouter
# from app.domain.schemas import EvaluationRequest
# from app.agents.graph_runner import run_vendor_evaluation

# router = APIRouter()

# @router.post("/")
# async def evaluate_vendor(req: EvaluationRequest):
#     result = await run_vendor_evaluation(
#         vendor_id=req.vendor_id,
#         query=req.query
#     )
#     return result
