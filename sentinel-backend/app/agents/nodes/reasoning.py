# app/agents/nodes/reasoning.py
import logging
from typing import Dict, List
from app.services.llm import gemini_structured_analysis

logger = logging.getLogger(__name__)

async def reason_over_context(state: Dict) -> Dict:
    vendor_id = state["vendor_id"]
    vendor_name = state.get("vendor_name", "Unknown")
    docs = state.get("retrieved_docs", [])

    result = await gemini_structured_analysis(vendor_name, docs)

    logger.info("reasoning.completed", extra={
        "vendor_id": vendor_id,
        "risks_count": len(result["extracted_risks"]),
        "frameworks_count": len(result["framework_mapping"]),
    })

    return {
        "extracted_risks": result["extracted_risks"],
        "framework_mapping": result["framework_mapping"],
        "reasoning_notes": result["reasoning_notes"],
    }