async def guardrail_check(state: dict) -> dict:
    """
    Enforces basic safety / compliance constraints.
    Can veto or modify execution later.
    """
    if not state["retrieved_docs"]:
        return {"final_assessment": "Insufficient data to assess vendor risk."}

    return {}
