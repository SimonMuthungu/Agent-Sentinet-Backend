from fastapi import APIRouter
from app.persistence.db import supabase

router = APIRouter()


@router.get("/")
def audit_log():
    """
    Immutable history of agent decisions.
    """
    return (
        supabase.table("agent_runs")
        .select("*")
        .order("created_at", desc=True)
        .execute()
        .data
    )
