from app.persistence.db import supabase
from typing import Dict, Any
import uuid


# --- AGENT MEMORY ---

def load_latest_vendor_state(vendor_id: str) -> Dict[str, Any] | None:
    """
    Loads the most recent agent state for a vendor.
    Used so the agent is stateful across runs.
    """
    res = (
        supabase.table("vendor_state")
        .select("state")
        .eq("vendor_id", vendor_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if res.data:
        return res.data[0]["state"]
    return None


def persist_vendor_state(vendor_id: str, state: Dict[str, Any]):
    """
    Persists updated agent state after a run.
    """
    supabase.table("vendor_state").insert({
        "vendor_id": vendor_id,
        "state": state
    }).execute()


# --- AGENT DECISIONS (AUDITABLE) ---

def record_agent_run(vendor_id: str, decision: str, confidence: float):
    """
    Immutable log of what the agent decided and how confident it was.
    This is your audit backbone.
    """
    supabase.table("agent_runs").insert({
        "vendor_id": vendor_id,
        "decision": decision,
        "confidence": confidence
    }).execute()


# --- VENDOR LIFECYCLE ---

def update_vendor_status(vendor_id: str, status: str):
    """
    Updates vendor status (ACTIVE, ESCALATED, BLOCKED, etc.)
    """
    supabase.table("vendors").update(
        {"status": status}
    ).eq("id", vendor_id).execute()


# --- ESCALATION ---

def create_escalation(
    vendor_id: str,
    reason: str,
    recommendation: str
):
    """
    Creates a HITL escalation when the agent is uncertain or flags risk.
    """
    supabase.table("escalations").insert({
        "vendor_id": vendor_id,
        "reason": reason,
        "recommendation": recommendation,
        "status": "OPEN"
    }).execute()
