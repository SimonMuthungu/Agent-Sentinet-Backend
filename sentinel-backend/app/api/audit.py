from fastapi import APIRouter
from app.persistence.db import supabase

router = APIRouter()


@router.get("/")
def list_audit_logs():
    """
    Returns all audit logs with full details.
    """
    res = (
        supabase
        .table("audit_log")
        .select("id, vendor_id, trigger, decision, confidence, created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data

