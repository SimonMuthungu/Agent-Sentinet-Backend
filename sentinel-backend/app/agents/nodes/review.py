# app/agents/nodes/review.py
import logging
from typing import Dict
from app.persistence.db import supabase
from datetime import datetime


logger = logging.getLogger(__name__)

def human_review(state: Dict) -> Dict:
    # This node doesn’t change the state; it marks that HITL is required and
    # ensures we carry forward all necessary context for UI rendering and audit.
    logger.info("review.ready", extra={
        "vendor_id": state["vendor_id"],
        "decision": state.get("decision"),
        "violations": [v["rule_id"] for v in state.get("policy_violations", [])],
    })

    placeholder_text = "HUMAN_REVIEW_REQUIRED"


    supabase.table("escalations").insert({
        "vendor_id": state["vendor_id"],
        "run_id": state.get("run_id"),  # ensure run_id is carried in state
        "decision": state.get("decision") or placeholder_text,
        "confidence": state.get("confidence"),
        "final_assessment": state.get("final_assessment") or placeholder_text,
        "recommended_actions": state.get("recommended_actions") or placeholder_text,
        "policy_violations": state.get("policy_violations") or [],
        "created_at": datetime.utcnow().isoformat(),
    }).execute()


    return {
        "human_review_required": True,
    }