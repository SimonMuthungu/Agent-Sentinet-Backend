from fastapi import APIRouter

router = APIRouter()

def escalation_router(state):
    if state.get("escalate"):
        return "review"
    return "synthesis"
