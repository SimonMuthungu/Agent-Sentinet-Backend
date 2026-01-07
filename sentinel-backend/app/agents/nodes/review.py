async def human_review(state: dict) -> dict:
    """
    HITL placeholder.
    Will trigger only when risk/confidence thresholds require it.
    """
    return {}

def review(state):
    return {
        "final_response": "Human review required",
        "decision": "ESCALATED"
    }
