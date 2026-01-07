from app.services.llm_service import synthesize

async def synthesize_response(state: dict) -> dict:
    context = "\n".join(state["retrieved_docs"])
    result = await synthesize(context, state["vendor_name"])
    return {"final_assessment": result}
