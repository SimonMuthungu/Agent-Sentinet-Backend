# app/agents/nodes/synthesis.py
import logging
from typing import Dict, List
from app.services.llm import gemini_executive_synthesis

logger = logging.getLogger(__name__)

async def synthesize_response(state: Dict) -> Dict:
    vendor_name = state.get("vendor_name", "Unknown")
    assessment = await gemini_executive_synthesis(
        vendor_name=vendor_name,
        extracted_risks=state.get("extracted_risks", []),
        framework_mapping=state.get("framework_mapping", []),
        policy_violations=state.get("policy_violations", []),
        retrieved_evidence=state.get("retrieved_evidence", []),
    )

    decision = assessment["decision"]
    confidence = assessment["confidence"]
    final_assessment = assessment["summary"]
    actions = assessment["recommended_actions"]

    logger.info("synthesis.completed", extra={
        "vendor_id": state["vendor_id"],
        "decision": decision,
        "confidence": confidence,
    })

    return {
        "decision": decision,
        "confidence": confidence,
        "final_assessment": final_assessment,
        "recommended_actions": actions,
        "human_review_required": decision != "APPROVED" or confidence < 0.7,
    }