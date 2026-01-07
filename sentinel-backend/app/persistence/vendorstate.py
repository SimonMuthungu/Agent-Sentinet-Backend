from app.persistence.db import supabase
from typing import Dict, Any
import uuid


def load_latest_vendor_state(vendor_id: str) -> Dict[str, Any] | None:
    res = (
        supabase.table("vendor_states")
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
    supabase.table("vendor_states").insert({
        "vendor_id": vendor_id,
        "state": state
    }).execute()


def record_agent_run(vendor_id: str, decision: str, confidence: float):
    supabase.table("agent_runs").insert({
        "vendor_id": vendor_id,
        "decision": decision,
        "confidence": confidence
    }).execute()


def update_vendor_status(vendor_id: str, status: str):
    supabase.table("vendors").update(
        {"status": status}
    ).eq("id", vendor_id).execute()

