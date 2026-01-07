from app.services.llm_service import synthesize

async def synthesize_response(state: dict) -> dict:
    context = "\n".join(state["retrieved_docs"])
    result = await synthesize(context, state["vendor_name"])
    return {"final_assessment": result}

def synthesize(state):
    decision = "APPROVED"
    if state["risk_score"] > 0.7:
        decision = "REVIEW_REQUIRED"

    return {
        "decision": decision,
        "final_response": f"Vendor decision: {decision}",
    }
