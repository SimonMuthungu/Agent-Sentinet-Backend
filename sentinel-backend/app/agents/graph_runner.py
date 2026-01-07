from app.agents.graph import executor
from app.persistence.vendorstate import (
    load_latest_vendor_state,
    persist_vendor_state,
    record_agent_run,
)

async def run_vendor_evaluation(vendor_id: str, query: str):
    state = load_latest_vendor_state(vendor_id) or {
        "vendor_id": vendor_id,
        "query": query,
        "history": [],
        "risk_score": 0.0,
        "confidence": 0.0,
        "escalate": False,
    }

    final_state = await executor.ainvoke(state)

    persist_vendor_state(vendor_id, final_state)
    record_agent_run(
        vendor_id,
        final_state.get("decision"),
        final_state.get("confidence", 0.0),
    )

    return final_state
