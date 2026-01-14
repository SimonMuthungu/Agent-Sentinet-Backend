from fastapi import APIRouter
from app.persistence.db import supabase

router = APIRouter()

def escalation_router(state):
    if state.get("escalate"):
        return "review"
    return "synthesis"

@router.get("/")
def list_open_escalations():
    """
    Returns all unresolved HITL escalations.
    """
    res = (
        supabase
        .table("escalations")
        .select(
            "id, vendor_id, run_id, decision, confidence, final_assessment, recommended_actions, policy_violations, status, created_at"
        )
        .eq("status", "open")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data


@router.post("/{escalation_id}/resolve")
def resolve_escalation(escalation_id: str):
    """
    Marks escalation as resolved after human decision.
    """
    supabase.table("escalations").update(
        {"status": "RESOLVED"}
    ).eq("id", escalation_id).execute()

    return {"status": "resolved"}


# app/api/escalations.py
def escalation_router(state: dict) -> str:
    # Route to human review if escalation is triggered, else proceed to synthesis
    if state.get("escalate") or state.get("human_review_required"):
        return "review"
    return "synthesis"
