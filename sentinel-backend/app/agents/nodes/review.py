# app/agents/nodes/review.py
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def human_review(state: Dict) -> Dict:
    # This node doesn’t change the state; it marks that HITL is required and
    # ensures we carry forward all necessary context for UI rendering and audit.
    logger.info("review.ready", extra={
        "vendor_id": state["vendor_id"],
        "decision": state.get("decision"),
        "violations": [v["rule_id"] for v in state.get("policy_violations", [])],
    })
    return {
        "human_review_required": True,
    }