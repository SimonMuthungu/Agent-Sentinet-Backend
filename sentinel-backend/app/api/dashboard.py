from fastapi import APIRouter
from app.persistence.db import supabase
from app.observability.logging import logger


router = APIRouter()

@router.get("/summary")
def dashboard_summary():
    vendors = supabase.table("vendors").select("id").execute().data
    escalations = supabase.table("escalations").select("id").eq("status", "open").execute().data
    audit = supabase.table("audit_log").select("id").execute().data

    summary = {
        "total_vendors": len(vendors),
        "active_escalations": len(escalations),
        "recent_risk_events": len(audit),
    }
    logger.info(f"Dashboard summary: {summary}")   # 👈 log to confirm
    return summary

