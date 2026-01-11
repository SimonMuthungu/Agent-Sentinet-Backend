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
        .table("vendor_states")
        .select("vendor_id, state, created_at")
        .contains("state", {"escalate": True})
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
