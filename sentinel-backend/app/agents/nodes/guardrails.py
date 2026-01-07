async def guardrail_check(state: dict) -> dict:
    """
    Enforces basic safety / compliance constraints.
    Can veto or modify execution later.
    """
    if not state["retrieved_docs"]:
        return {"final_assessment": "Insufficient data to assess vendor risk."}

    return {}

def guardrails(state):
    if not state.get("documents_complete", True):
        return {
            "escalate": True,
            "reason": "Missing mandatory documents"
        }
    return {}
